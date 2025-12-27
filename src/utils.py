"""
Module: utils.py
References: Task T006, Spec §Requirements
"""
from typing import Union


def validate_title(title: str) -> bool:
    """Validate that the title meets the requirements (1-100 characters).

    Args:
        title: The title to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(title, str):
        return False
    
    # Check length (1-100 characters)
    if not (1 <= len(title) <= 100):
        return False
    
    # Check if title is not empty or whitespace-only
    if not title.strip():
        return False
    
    return True


def validate_description(description: str) -> bool:
    """Validate that the description meets the requirements (0-500 characters).

    Args:
        description: The description to validate

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(description, str):
        return False
    
    # Check length (0-500 characters)
    if len(description) > 500:
        return False
    
    return True


def validate_task_id(task_id: Union[str, int]) -> bool:
    """Validate that the task ID is a positive integer.

    Args:
        task_id: The task ID to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        # Convert to int if it's a string
        if isinstance(task_id, str):
            task_id = int(task_id)
        
        # Check if it's a positive integer
        return isinstance(task_id, int) and task_id > 0
    except ValueError:
        return False