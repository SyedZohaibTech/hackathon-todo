"""
MCP (Model Context Protocol) Server for Todo Application
This server exposes task operations as tools for AI agents to use.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
import json
from ..database.database import get_session, create_db_and_tables
from ..services.task_service import TaskService
from ..services.user_service import UserService
from ..models.task import TaskCreate, TaskUpdate


app = FastAPI(title="Todo MCP Server", version="1.0.0")


class TaskCreateRequest(BaseModel):
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    user_id: str = Field(..., description="ID of the user creating the task")
    completed: bool = Field(False, description="Whether the task is completed")
    due_date: Optional[str] = Field(None, description="Due date for the task")
    priority: int = Field(1, ge=1, le=5, description="Priority level (1-5)")


class TaskUpdateRequest(BaseModel):
    task_id: str = Field(..., description="ID of the task to update")
    user_id: str = Field(..., description="ID of the user updating the task")
    title: Optional[str] = Field(None, description="New title of the task")
    description: Optional[str] = Field(None, description="New description of the task")
    completed: Optional[bool] = Field(None, description="New completion status")
    due_date: Optional[str] = Field(None, description="New due date for the task")
    priority: Optional[int] = Field(None, ge=1, le=5, description="New priority level")


class TaskIdRequest(BaseModel):
    task_id: str = Field(..., description="ID of the task")
    user_id: str = Field(..., description="ID of the user performing the action")


class UserIdRequest(BaseModel):
    user_id: str = Field(..., description="ID of the user")


@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()


@app.post("/tools/create_task")
async def create_task_endpoint(request: TaskCreateRequest):
    """MCP endpoint to create a new task"""
    try:
        # Convert string user_id to UUID
        user_id = UUID(request.user_id)

        # Create task data
        task_create = TaskCreate(
            title=request.title,
            description=request.description,
            completed=request.completed,
            due_date=request.due_date,
            priority=request.priority
        )

        # Get database session and create task
        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.create_task(task_create, user_id)

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tools/get_tasks")
async def get_tasks_endpoint(request: UserIdRequest):
    """MCP endpoint to get all tasks for a user"""
    try:
        # Convert string user_id to UUID
        user_id = UUID(request.user_id)

        # Get database session and fetch tasks
        with next(get_session()) as session:
            task_service = TaskService(session)
            tasks = task_service.get_tasks_by_user(user_id)

        # Convert tasks to JSON-serializable format
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority
            })

        return {
            "success": True,
            "tasks": tasks_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tools/update_task")
async def update_task_endpoint(request: TaskUpdateRequest):
    """MCP endpoint to update a task"""
    try:
        # Convert string IDs to UUIDs
        task_id = UUID(request.task_id)
        user_id = UUID(request.user_id)

        # Create task update data
        task_update = TaskUpdate(
            title=request.title,
            description=request.description,
            completed=request.completed,
            due_date=request.due_date,
            priority=request.priority
        )

        # Get database session and update task
        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.update_task(task_id, task_update, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tools/delete_task")
async def delete_task_endpoint(request: TaskIdRequest):
    """MCP endpoint to delete a task"""
    try:
        # Convert string IDs to UUIDs
        task_id = UUID(request.task_id)
        user_id = UUID(request.user_id)

        # Get database session and delete task
        with next(get_session()) as session:
            task_service = TaskService(session)
            success = task_service.delete_task(task_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "task_id": request.task_id,
            "message": "Task deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tools/mark_task_completed")
async def mark_task_completed_endpoint(request: TaskIdRequest):
    """MCP endpoint to mark a task as completed"""
    try:
        # Convert string IDs to UUIDs
        task_id = UUID(request.task_id)
        user_id = UUID(request.user_id)

        # Get database session and mark task as completed
        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.mark_task_completed(task_id, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' marked as completed"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/tools/mark_task_incomplete")
async def mark_task_incomplete_endpoint(request: TaskIdRequest):
    """MCP endpoint to mark a task as incomplete"""
    try:
        # Convert string IDs to UUIDs
        task_id = UUID(request.task_id)
        user_id = UUID(request.user_id)

        # Get database session and mark task as incomplete
        with next(get_session()) as session:
            task_service = TaskService(session)
            task = task_service.mark_task_incomplete(task_id, user_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "success": True,
            "task_id": str(task.id),
            "message": f"Task '{task.title}' marked as incomplete"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Todo MCP Server is running!"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "mcp-server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)