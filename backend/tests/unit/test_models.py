import pytest
from uuid import UUID
from datetime import datetime
from src.models.task import Task, TaskCreate
from src.models.user import User, UserCreate


def test_task_creation():
    """Test creating a task model"""
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        priority=1
    )

    assert task_data.title == "Test Task"
    assert task_data.description == "Test Description"
    assert task_data.completed == False
    assert task_data.priority == 1


def test_user_creation():
    """Test creating a user model"""
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        password="securepassword",
        first_name="Test",
        last_name="User"
    )

    assert user_data.email == "test@example.com"
    assert user_data.username == "testuser"
    assert user_data.password == "securepassword"
    assert user_data.first_name == "Test"
    assert user_data.last_name == "User"


if __name__ == "__main__":
    test_task_creation()
    test_user_creation()
    print("All model tests passed!")