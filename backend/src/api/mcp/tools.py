"""
MCP (Model Context Protocol) Tools for Todo Application
These tools are exposed for AI agents to perform task operations.
"""

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from ...database.database import get_session
from ...services.task_service import TaskService
from ...models.task import TaskCreate, TaskUpdate


class TaskCreateSchema(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    user_id: str = Field(..., description="ID of the user creating the task")
    completed: bool = Field(False, description="Whether the task is completed")
    due_date: Optional[str] = Field(None, description="Due date for the task")
    priority: int = Field(1, ge=1, le=5, description="Priority level (1-5)")


class TaskUpdateSchema(BaseModel):
    task_id: str = Field(..., description="ID of the task to update")
    user_id: str = Field(..., description="ID of the user updating the task")
    title: Optional[str] = Field(None, description="New title of the task")
    description: Optional[str] = Field(None, description="New description of the task")
    completed: Optional[bool] = Field(None, description="New completion status")
    due_date: Optional[str] = Field(None, description="New due date for the task")
    priority: Optional[int] = Field(None, ge=1, le=5, description="New priority level")


class TaskIdSchema(BaseModel):
    task_id: str = Field(..., description="ID of the task")
    user_id: str = Field(..., description="ID of the user performing the action")


class UserIdSchema(BaseModel):
    user_id: str = Field(..., description="ID of the user")


def create_task(title: str, description: str, user_id: str, completed: bool = False, due_date: str = None, priority: int = 1) -> dict:
    """
    Create a new task for a user.

    Args:
        title: Title of the task
        description: Description of the task
        user_id: ID of the user creating the task
        completed: Whether the task is completed (default: False)
        due_date: Due date for the task (optional)
        priority: Priority level (1-5, default: 1)

    Returns:
        Dictionary with success status and task ID
    """
    try:
        user_uuid = UUID(user_id)

        task_create = TaskCreate(
            title=title,
            description=description,
            completed=completed,
            due_date=due_date,
            priority=priority
        )

        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.create_task(task_create, user_uuid)

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to create task"
        }


def get_tasks(user_id: str) -> dict:
    """
    Get all tasks for a user.

    Args:
        user_id: ID of the user

    Returns:
        Dictionary with success status and list of tasks
    """
    try:
        user_uuid = UUID(user_id)

        with next(get_session()) as session:
            task_service = TaskService(session)
            tasks = task_service.get_tasks_by_user(user_uuid)

        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority
            })

        return {
            "success": True,
            "tasks": tasks_data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get tasks"
        }


def update_task(task_id: str, user_id: str, title: str = None, description: str = None,
                completed: bool = None, due_date: str = None, priority: int = None) -> dict:
    """
    Update a task for a user.

    Args:
        task_id: ID of the task to update
        user_id: ID of the user updating the task
        title: New title of the task (optional)
        description: New description of the task (optional)
        completed: New completion status (optional)
        due_date: New due date for the task (optional)
        priority: New priority level (optional)

    Returns:
        Dictionary with success status and updated task info
    """
    try:
        task_uuid = UUID(task_id)
        user_uuid = UUID(user_id)

        task_update = TaskUpdate(
            title=title,
            description=description,
            completed=completed,
            due_date=due_date,
            priority=priority
        )

        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.update_task(task_uuid, task_update, user_uuid)

        if not task:
            return {
                "success": False,
                "message": "Task not found"
            }

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' updated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to update task"
        }


def delete_task(task_id: str, user_id: str) -> dict:
    """
    Delete a task for a user.

    Args:
        task_id: ID of the task to delete
        user_id: ID of the user deleting the task

    Returns:
        Dictionary with success status
    """
    try:
        task_uuid = UUID(task_id)
        user_uuid = UUID(user_id)

        with next(get_session()) as session:
            task_service = TaskService(session)
            success = task_service.delete_task(task_uuid, user_uuid)

        if not success:
            return {
                "success": False,
                "message": "Task not found"
            }

        return {
            "success": True,
            "message": "Task deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to delete task"
        }


def mark_task_completed(task_id: str, user_id: str) -> dict:
    """
    Mark a task as completed for a user.

    Args:
        task_id: ID of the task to mark as completed
        user_id: ID of the user marking the task as completed

    Returns:
        Dictionary with success status and updated task info
    """
    try:
        task_uuid = UUID(task_id)
        user_uuid = UUID(user_id)

        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.mark_task_completed(task_uuid, user_uuid)

        if not task:
            return {
                "success": False,
                "message": "Task not found"
            }

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' marked as completed"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to mark task as completed"
        }


def mark_task_incomplete(task_id: str, user_id: str) -> dict:
    """
    Mark a task as incomplete for a user.

    Args:
        task_id: ID of the task to mark as incomplete
        user_id: ID of the user marking the task as incomplete

    Returns:
        Dictionary with success status and updated task info
    """
    try:
        task_uuid = UUID(task_id)
        user_uuid = UUID(user_id)

        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.mark_task_incomplete(task_uuid, user_uuid)

        if not task:
            return {
                "success": False,
                "message": "Task not found"
            }

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' marked as incomplete"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to mark task as incomplete"
        }