from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import UUID
from ...middleware.auth_middleware import auth_middleware
from ...services.task_service import TaskService
from ...database.database import get_session
from sqlmodel import Session
import os
import sys
import re
from ...models.task import TaskCreate

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


def create_basic_task_from_request(message: str, user_id: UUID, session: Session) -> str:
    """
    Create a basic task from the user's request when AI is unavailable.
    This ensures database write happens unconditionally.
    """
    patterns = [
        r'add\s+(?:a\s+|an\s+)?(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
        r'create\s+(?:a\s+|an\s+)?(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
        r'new\s+(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
        r'add\s+"?([^"]+?)"?\s+(?:as\s+a\s+)?task',
        r'create\s+"?([^"]+?)"?\s+(?:as\s+a\s+)?task',
        r'add\s+(?!a\s|an\s)([^,.!?]+?)(?:\s|$)',
    ]

    task_title = None
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            task_title = match.group(1).strip()
            if task_title.startswith("to "):
                task_title = task_title[3:]
            task_title = task_title.capitalize()
            break

    if not task_title:
        parts = re.split(r'[.!?]', message.strip(), 1)
        task_title = parts[0].strip()[:50].capitalize()

    task_service = TaskService(session)
    task_create = TaskCreate(
        title=task_title,
        description=message,
        completed=False,
        priority=1
    )

    try:
        task = task_service.create_task(task_create, user_id)
        return f"Task '{task.title}' created successfully in database."
    except Exception as e:
        return f"Failed to create task in database: {str(e)}"


@router.post("/process", response_model=ChatResponse)
def process_chat(
    request: ChatRequest,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Process natural language requests using the AI agent.
    If AI fails, create a basic task instead.
    """
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            # If AI API key is missing, just create the task
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=response)

        # Attempt to use TodoAgent
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
        agent_src_path = os.path.join(project_root, "agent", "src")

        if agent_src_path not in sys.path:
            sys.path.insert(0, agent_src_path)

        try:
            from agents.todo_agent import TodoAgent
            agent = TodoAgent()
            response = agent.process_request(request.message, str(current_user_id))
            return ChatResponse(response=response)
        except ImportError:
            # Fallback if agent not installed
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=response)  # ✅ bracket removed
        except Exception as e:
            # Fallback if AI fails for any other reason
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=response)
        finally:
            if agent_src_path in sys.path:
                sys.path.remove(agent_src_path)

    except Exception as e:
        # General fallback
        try:
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=response)
        except Exception as db_error:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing chat request and creating task: {str(db_error)}"
            )
