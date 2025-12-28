"""
API response format utilities
References: Task T212, Spec §X
"""
from typing import Any, Dict
from fastapi import HTTPException, status

def create_success_response(data: Any = None) -> Dict[str, Any]:
    """
    Create a standardized success response
    Args:
        data: The data to include in the response
    Returns:
        Dictionary with success status and data
    """
    return {
        "success": True,
        "data": data
    }

def create_error_response(error: str) -> Dict[str, Any]:
    """
    Create a standardized error response
    Args:
        error: The error message
    Returns:
        Dictionary with error status and message
    """
    return {
        "success": False,
        "error": error
    }

def raise_http_exception(status_code: int, detail: str) -> HTTPException:
    """
    Create and return an HTTP exception
    Args:
        status_code: The HTTP status code
        detail: The error detail
    Returns:
        HTTPException instance
    """
    return HTTPException(
        status_code=status_code,
        detail=create_error_response(detail)
    )