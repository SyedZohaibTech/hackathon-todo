"""
Task management routes
References: Task T233, Spec §X
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from backend.db import get_session
from backend.models import Task, TaskCreate, TaskRead, User
from backend.middleware.jwt_middleware import verify_token
from backend.utils import create_success_response
from uuid import UUID

router = APIRouter()

@router.post("/{user_id}/tasks", response_model=dict)
def create_task(
    user_id: UUID,
    task: TaskCreate,
    current_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user
    Args:
        user_id: The ID of the user to create the task for
        task: Task creation data (title, description)
        current_user_id: The ID of the currently authenticated user
        session: Database session
    Returns:
        Success response with created task
    Raises:
        HTTPException: If user IDs don't match or other error occurs
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Verify that the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create the new task
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        user_id=user_id
    )

    # Add to database
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Return success response with task data
    task_data = TaskRead.from_orm(db_task) if hasattr(Task, "from_orm") else TaskRead(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed
    )
    return create_success_response(task_data)

@router.get("/{user_id}/tasks", response_model=dict)
def read_tasks(
    user_id: UUID,
    current_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user
    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user_id: The ID of the currently authenticated user
        session: Database session
    Returns:
        Success response with list of tasks
    Raises:
        HTTPException: If user IDs don't match
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view tasks for this user"
        )

    # Query tasks for the user
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()

    # Convert to response format
    tasks_data = []
    for task in tasks:
        task_data = TaskRead.from_orm(task) if hasattr(Task, "from_orm") else TaskRead(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed
        )
        tasks_data.append(task_data)

    return create_success_response(tasks_data)

@router.put("/{user_id}/tasks/{id}", response_model=dict)
def update_task(
    user_id: UUID,
    id: int,
    task: TaskCreate,
    current_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Update an existing task for the specified user
    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to update
        task: Task update data (title, description)
        current_user_id: The ID of the currently authenticated user
        session: Database session
    Returns:
        Success response with updated task
    Raises:
        HTTPException: If user IDs don't match, task not found, or not authorized
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update tasks for this user"
        )

    # Get the existing task
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the specified user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Update the task
    db_task.title = task.title
    db_task.description = task.description

    # Commit changes to database
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Return success response with updated task data
    task_data = TaskRead.from_orm(db_task) if hasattr(Task, "from_orm") else TaskRead(
        id=db_task.id,
        user_id=db_task.user_id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed
    )
    return create_success_response(task_data)

@router.delete("/{user_id}/tasks/{id}", response_model=dict)
def delete_task(
    user_id: UUID,
    id: int,
    current_user_id: str = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Delete an existing task for the specified user
    Args:
        user_id: The ID of the user who owns the task
        id: The ID of the task to delete
        current_user_id: The ID of the currently authenticated user
        session: Database session
    Returns:
        Success response confirming deletion
    Raises:
        HTTPException: If user IDs don't match, task not found, or not authorized
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(user_id) != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete tasks for this user"
        )
    
    # Get the existing task
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Verify that the task belongs to the specified user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    # Delete the task
    session.delete(db_task)
    session.commit()
    
    # Return success response
    return create_success_response({"message": "Task deleted successfully"})