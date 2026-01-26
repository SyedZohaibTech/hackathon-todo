"""
MCP Client for the Todo Agent
Provides an interface to communicate with the MCP server for task operations
"""
import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel


class TaskOperationResult(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class MCPClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip('/')

    def _make_request(self, endpoint: str, data: Dict[str, Any]) -> TaskOperationResult:
        """Make a request to the MCP server"""
        try:
            response = requests.post(
                f"{self.base_url}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                result = response.json()
                return TaskOperationResult(**result)
            else:
                return TaskOperationResult(
                    success=False,
                    message=f"HTTP {response.status_code}: {response.text}"
                )
        except Exception as e:
            return TaskOperationResult(
                success=False,
                message=f"Connection error: {str(e)}"
            )

    def create_task(self, title: str, description: str, user_id: str,
                    completed: bool = False, due_date: str = None, priority: int = 1) -> TaskOperationResult:
        """Create a new task"""
        data = {
            "title": title,
            "description": description,
            "user_id": user_id,
            "completed": completed,
            "due_date": due_date,
            "priority": priority
        }

        return self._make_request("/tools/create_task", data)

    def get_tasks(self, user_id: str) -> TaskOperationResult:
        """Get all tasks for a user"""
        data = {"user_id": user_id}

        return self._make_request("/tools/get_tasks", data)

    def update_task(self, task_id: str, user_id: str, title: str = None,
                   description: str = None, completed: bool = None,
                   due_date: str = None, priority: int = None) -> TaskOperationResult:
        """Update a task"""
        data = {
            "task_id": task_id,
            "user_id": user_id
        }

        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if completed is not None:
            data["completed"] = completed
        if due_date is not None:
            data["due_date"] = due_date
        if priority is not None:
            data["priority"] = priority

        return self._make_request("/tools/update_task", data)

    def delete_task(self, task_id: str, user_id: str) -> TaskOperationResult:
        """Delete a task"""
        data = {
            "task_id": task_id,
            "user_id": user_id
        }

        return self._make_request("/tools/delete_task", data)

    def mark_task_completed(self, task_id: str, user_id: str) -> TaskOperationResult:
        """Mark a task as completed"""
        data = {
            "task_id": task_id,
            "user_id": user_id
        }

        return self._make_request("/tools/mark_task_completed", data)

    def mark_task_incomplete(self, task_id: str, user_id: str) -> TaskOperationResult:
        """Mark a task as incomplete"""
        data = {
            "task_id": task_id,
            "user_id": user_id
        }

        return self._make_request("/tools/mark_task_incomplete", data)