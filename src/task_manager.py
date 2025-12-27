"""
Module: task_manager.py
References: Task T003, T004, Spec §Requirements
"""
from datetime import datetime
from typing import Dict, List, Optional
from models import Task


class TaskManager:
    """
    Manages the collection of tasks with CRUD operations.
    """

    def __init__(self):
        """Initialize the task manager with empty storage."""
        self.storage: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task with the given title and description.

        Args:
            title: Required title (1-100 characters)
            description: Optional description (0-500 characters)

        Returns:
            The created Task object

        Raises:
            ValueError: If title doesn't meet validation requirements
        """
        # Validate title length (1-100 characters)
        if not (1 <= len(title) <= 100):
            raise ValueError("Title must be between 1 and 100 characters")

        # Validate description length (0-500 characters)
        if len(description) > 500:
            raise ValueError("Description must be 0 to 500 characters")

        # Validate title is not empty or whitespace-only
        if not title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        # Create new task with unique ID and current timestamp
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now()
        )

        # Add task to storage
        self.storage[task.id] = task

        # Increment next_id for the next task
        self.next_id += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the storage.

        Returns:
            List of all Task objects
        """
        # Return all tasks from storage as a list
        # Using list() to create a copy to prevent external modification
        return list(self.storage.values())

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> bool:
        """Update an existing task with new values.

        Args:
            task_id: ID of the task to update
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            True if task was updated, False if task not found
        """
        # Check if task exists in storage
        if task_id not in self.storage:
            return False

        # Get the existing task
        task = self.storage[task_id]

        # Use existing values if new values are not provided
        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        # Validate the new values if they are being updated
        if title is not None:
            # Validate title length (1-100 characters)
            if not (1 <= len(new_title) <= 100):
                raise ValueError("Title must be between 1 and 100 characters")

            # Validate title is not empty or whitespace-only
            if not new_title.strip():
                raise ValueError("Title cannot be empty or contain only whitespace")

        if description is not None:
            # Validate description length (0-500 characters)
            if len(new_description) > 500:
                raise ValueError("Description must be 0 to 500 characters")

        # Update the task with new values
        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            completed=task.completed,
            created_at=task.created_at
        )

        # Replace the task in storage
        self.storage[task_id] = updated_task

        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        # Check if task exists in storage
        if task_id not in self.storage:
            return False

        # Remove task from storage
        del self.storage[task_id]

        return True

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            True if task status was toggled, False if task not found
        """
        # Check if task exists in storage
        if task_id not in self.storage:
            return False

        # Get the existing task
        task = self.storage[task_id]

        # Toggle the completion status
        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=not task.completed,  # Toggle the status
            created_at=task.created_at
        )

        # Replace the task in storage
        self.storage[task_id] = updated_task

        return True