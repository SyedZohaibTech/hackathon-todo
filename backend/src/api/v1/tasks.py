from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ...database.database import get_session
from ...models.task import TaskRead, TaskCreate, TaskUpdate
from ...services.task_service import TaskService
from ...middleware.auth_middleware import auth_middleware

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def get_tasks(
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get all tasks for the current user"""
    task_service = TaskService(session)
    tasks = task_service.get_tasks_by_user(current_user_id)
    return tasks


@router.post("/", response_model=TaskRead)
def create_task(
    task_create: TaskCreate,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a new task for the current user"""
    task_service = TaskService(session)
    task = task_service.create_task(task_create, current_user_id)
    return task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: UUID,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Get a specific task by ID"""
    task_service = TaskService(session)
    task = task_service.get_task_by_id(task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update a specific task"""
    task_service = TaskService(session)
    task = task_service.update_task(task_id, task_update, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{task_id}")
def delete_task(
    task_id: UUID,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Delete a specific task"""
    task_service = TaskService(session)
    success = task_service.delete_task(task_id, current_user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskRead)
def mark_task_complete(
    task_id: UUID,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Mark a task as complete"""
    task_service = TaskService(session)
    task = task_service.mark_task_completed(task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.patch("/{task_id}/incomplete", response_model=TaskRead)
def mark_task_incomplete(
    task_id: UUID,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """Mark a task as incomplete"""
    task_service = TaskService(session)
    task = task_service.mark_task_incomplete(task_id, current_user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task