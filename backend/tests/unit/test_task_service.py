import pytest
from unittest.mock import Mock, MagicMock
from uuid import UUID, uuid4
from src.models.task import TaskCreate
from src.services.task_service import TaskService


def test_create_task():
    """Test creating a task"""
    # Create a mock session
    session_mock = Mock()

    # Create task service instance
    task_service = TaskService(session_mock)

    # Create test data
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        completed=False,
        priority=1
    )
    user_id = uuid4()

    # Mock the session.add and session.commit methods
    session_mock.add = Mock()
    session_mock.commit = Mock()
    session_mock.refresh = Mock()

    # Create a mock task object to return
    mock_task = Mock()
    mock_task.id = uuid4()
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.priority = 1
    mock_task.user_id = user_id

    # Patch the task creation to return our mock
    from unittest.mock import patch
    with patch('src.models.task.Task') as task_constructor:
        task_constructor.return_value = mock_task
        result = task_service.create_task(task_data, user_id)

        # Verify that session methods were called
        session_mock.add.assert_called_once()
        session_mock.commit.assert_called_once()
        session_mock.refresh.assert_called_once()

        # Verify the result
        assert result.id == mock_task.id
        assert result.title == "Test Task"


def test_get_tasks_by_user():
    """Test getting tasks for a specific user"""
    # Create a mock session
    session_mock = Mock()
    task_service = TaskService(session_mock)

    # Create test data
    user_id = uuid4()

    # Mock the database query
    from sqlmodel import select
    from src.models.task import Task

    # Create mock tasks
    mock_task1 = Mock()
    mock_task1.id = uuid4()
    mock_task1.title = "Task 1"
    mock_task1.completed = False

    mock_task2 = Mock()
    mock_task2.id = uuid4()
    mock_task2.title = "Task 2"
    mock_task2.completed = True

    # Mock the exec method to return our tasks
    exec_mock = Mock()
    exec_mock.all.return_value = [mock_task1, mock_task2]
    session_mock.exec.return_value = exec_mock

    result = task_service.get_tasks_by_user(user_id)

    # Verify the query was constructed correctly
    session_mock.exec.assert_called_once()

    # Verify the results
    assert len(result) == 2
    assert result[0].title == "Task 1"
    assert result[1].title == "Task 2"


if __name__ == "__main__":
    test_create_task()
    test_get_tasks_by_user()
    print("All task service tests passed!")