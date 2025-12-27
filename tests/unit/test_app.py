"""
Module: test_app.py
Simple tests for the Todo Console App
"""
import sys
import os
# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.task_manager import TaskManager
from src.models import Task
from datetime import datetime


def test_task_creation():
    """Test creating a task with valid inputs."""
    print("Testing task creation...")

    task_manager = TaskManager()

    # Test adding a task with valid title and description
    task = task_manager.add_task("Test Task", "This is a test description")

    assert task.id == 1, f"Expected ID 1, got {task.id}"
    assert task.title == "Test Task", f"Expected title 'Test Task', got {task.title}"
    assert task.description == "This is a test description", f"Expected description 'This is a test description', got {task.description}"
    assert task.completed == False, f"Expected completed False, got {task.completed}"
    assert isinstance(task.created_at, datetime), f"Expected datetime, got {type(task.created_at)}"

    print("PASS Task creation test passed")


def test_task_retrieval():
    """Test retrieving all tasks."""
    print("Testing task retrieval...")

    task_manager = TaskManager()

    # Add a few tasks
    task_manager.add_task("Task 1", "Description 1")
    task_manager.add_task("Task 2", "Description 2")

    # Retrieve all tasks
    tasks = task_manager.get_all_tasks()

    assert len(tasks) == 2, f"Expected 2 tasks, got {len(tasks)}"

    # Check that the tasks have the expected properties
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"

    print("PASS Task retrieval test passed")


def test_task_update():
    """Test updating a task."""
    print("Testing task update...")

    task_manager = TaskManager()

    # Add a task
    original_task = task_manager.add_task("Original Task", "Original description")
    original_id = original_task.id

    # Update the task
    success = task_manager.update_task(original_id, "Updated Task", "Updated description")

    assert success == True, f"Expected update to succeed, got {success}"

    # Retrieve the updated task
    updated_task = task_manager.storage[original_id]

    assert updated_task.title == "Updated Task", f"Expected title 'Updated Task', got {updated_task.title}"
    assert updated_task.description == "Updated description", f"Expected description 'Updated description', got {updated_task.description}"

    print("PASS Task update test passed")


def test_task_deletion():
    """Test deleting a task."""
    print("Testing task deletion...")

    task_manager = TaskManager()

    # Add a task
    task = task_manager.add_task("Task to delete", "Description")
    task_id = task.id

    # Verify the task exists
    assert task_id in task_manager.storage, f"Task with ID {task_id} should exist in storage"

    # Delete the task
    success = task_manager.delete_task(task_id)

    assert success == True, f"Expected deletion to succeed, got {success}"
    assert task_id not in task_manager.storage, f"Task with ID {task_id} should not exist in storage after deletion"

    print("PASS Task deletion test passed")


def test_task_completion_toggle():
    """Test toggling task completion status."""
    print("Testing task completion toggle...")

    task_manager = TaskManager()

    # Add a task
    task = task_manager.add_task("Task to toggle", "Description")
    task_id = task.id

    # Verify the task is initially incomplete
    assert task_manager.storage[task_id].completed == False, f"Expected task to be incomplete initially, got {task_manager.storage[task_id].completed}"

    # Toggle completion status
    success = task_manager.toggle_complete(task_id)

    assert success == True, f"Expected toggle to succeed, got {success}"
    assert task_manager.storage[task_id].completed == True, f"Expected task to be complete after toggle, got {task_manager.storage[task_id].completed}"

    # Toggle again to make it incomplete
    success = task_manager.toggle_complete(task_id)

    assert success == True, f"Expected second toggle to succeed, got {success}"
    assert task_manager.storage[task_id].completed == False, f"Expected task to be incomplete after second toggle, got {task_manager.storage[task_id].completed}"

    print("PASS Task completion toggle test passed")


def test_validation():
    """Test input validation."""
    print("Testing input validation...")

    task_manager = TaskManager()

    # Test title too short
    try:
        task_manager.add_task("", "Description")
        assert False, "Expected ValueError for empty title"
    except ValueError:
        pass  # Expected

    # Test title too long
    try:
        long_title = "A" * 101  # 101 characters, exceeding the limit
        task_manager.add_task(long_title, "Description")
        assert False, "Expected ValueError for title too long"
    except ValueError:
        pass  # Expected

    # Test description too long
    try:
        long_description = "A" * 501  # 501 characters, exceeding the limit
        task_manager.add_task("Valid Title", long_description)
        assert False, "Expected ValueError for description too long"
    except ValueError:
        pass  # Expected

    print("PASS Input validation test passed")


def run_all_tests():
    """Run all tests."""
    print("Running comprehensive tests for Todo Console App...\n")

    test_task_creation()
    test_task_retrieval()
    test_task_update()
    test_task_deletion()
    test_task_completion_toggle()
    test_validation()

    print("\nPASS All tests passed! The application is working correctly.")


if __name__ == "__main__":
    run_all_tests()