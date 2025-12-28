"""
Database models using SQLModel
References: Task T202, Spec §X
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID, uuid4
import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None, max_length=100)

class User(UserBase, table=True):
    """
    User model with email, name, and password hash
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    password_hash: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: UUID

    class Config:
        from_attributes = True

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    """
    Task model with title, description, and completion status
    """
    id: int = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: UUID