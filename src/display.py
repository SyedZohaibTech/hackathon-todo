"""
Module: display.py
References: Task T007, Spec §Requirements
"""
from typing import List
from models import Task


def format_task(task: Task) -> str:
    """Format a single task for display.

    Args:
        task: The task to format

    Returns:
        Formatted string representation of the task
    """
    status = "Complete" if task.completed else "Incomplete"
    return f"ID: {task.id} | Title: {task.title} | Status: {status} | Description: {task.description}"


def format_tasks_list(tasks: List[Task]) -> str:
    """Format a list of tasks for display.

    Args:
        tasks: The list of tasks to format

    Returns:
        Formatted string representation of the tasks list with count summary
    """
    if not tasks:
        return "No tasks found"
    
    formatted_tasks = []
    for task in tasks:
        formatted_tasks.append(format_task(task))
    
    result = "\n".join(formatted_tasks)
    result += f"\nTotal tasks: {len(tasks)}"
    
    return result


def format_error_message(message: str) -> str:
    """Format an error message for user display.

    Args:
        message: The error message to format

    Returns:
        Formatted error message
    """
    return f"Error: {message}"