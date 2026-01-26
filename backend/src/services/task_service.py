from typing import List, Optional
from sqlmodel import Session, select
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_data: TaskCreate, user_id: UUID) -> Task:
        """Create a new task for a specific user"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            due_date=task_data.due_date,
            priority=task_data.priority,
            user_id=user_id
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Get a specific task by ID for a specific user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return self.session.execute(statement).scalar()

    def get_tasks_by_user(self, user_id: UUID) -> List[Task]:
        """Get all tasks for a specific user"""
        statement = select(Task).where(Task.user_id == user_id)
        return self.session.execute(statement).scalars().all()

    def update_task(self, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
        """Update a specific task for a specific user"""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        # Update fields that are provided
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """Delete a specific task for a specific user"""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def mark_task_completed(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Mark a specific task as completed for a specific user"""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        task.completed = True
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def mark_task_incomplete(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """Mark a specific task as incomplete for a specific user"""
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        task.completed = False
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task