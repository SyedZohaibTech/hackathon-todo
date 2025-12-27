"""
Module: models.py
References: Task T002, Spec §Key Entities
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a single todo item.
    
    Attributes:
        id: Unique identifier for the task (integer)
        title: Required title with 1-100 characters
        description: Optional description with 0-500 characters
        completed: Boolean indicating completion status
        created_at: Timestamp of when the task was created
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    def __post_init__(self):
        """Validate task fields after initialization."""
        # Validate title length (1-100 characters)
        if not (1 <= len(self.title) <= 100):
            raise ValueError("Title must be between 1 and 100 characters")
        
        # Validate description length (0-500 characters)
        if len(self.description) > 500:
            raise ValueError("Description must be 0 to 500 characters")
        
        # Validate title is not empty or whitespace-only
        if not self.title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")