from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from uuid import UUID
from ...middleware.auth_middleware import auth_middleware
from ...services.task_service import TaskService
from ...database.database import get_session
from sqlmodel import Session
import os
import requests
from ...models.user import UserRead

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/process", response_model=ChatResponse)
def process_chat(
    request: ChatRequest,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Process natural language requests using the AI agent.
    This endpoint connects the frontend to the AI agent for task management.
    """
    try:
        # Import the TodoAgent if available, but don't fail if it's not
        import subprocess
        import sys

        # Get the project root directory (two levels up from this file)
        current_dir = os.path.dirname(__file__)
        project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
        agent_src_path = os.path.join(project_root, "agent", "src")

        # Add the agent src path to sys.path
        original_path = sys.path[:]
        if agent_src_path not in sys.path:
            sys.path.insert(0, agent_src_path)

        try:
            # Import the TodoAgent
            from agents.todo_agent import TodoAgent

            # Initialize the agent
            agent = TodoAgent()

            # Process the request with the agent - this ensures task creation happens first
            response = agent.process_request(request.message, str(current_user_id))

            return ChatResponse(response=response)
        except ImportError:
            # If agent is not available, try to parse and create a basic task
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=response)
        except Exception as e:
            # Check if it's an OpenAI API error with quota issues
            error_msg = str(e)
            if "insufficient_quota" in error_msg.lower() or "429" in error_msg:
                # Even if AI fails, try to create the task directly
                response = create_basic_task_from_request(request.message, current_user_id, session)
                return ChatResponse(response=f"{response} (AI enhancement unavailable due to quota limits)")
            else:
                # Even if AI fails, try to create the task directly
                response = create_basic_task_from_request(request.message, current_user_id, session)
                return ChatResponse(response=f"{response} (AI enhancement unavailable: {str(e)})")
        finally:
            # Restore original path
            sys.path[:] = original_path

    except Exception as e:
        # Fallback: create basic task even if everything else fails
        try:
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=f"{response} (Processing error occurred: {str(e)})")
        except Exception as db_error:
            raise HTTPException(status_code=500, detail=f"Error processing chat request and creating task: {str(db_error)}")


def create_basic_task_from_request(message: str, user_id: UUID, session: Session) -> str:
    """
    Create a basic task from the user's request when AI is unavailable.
    This ensures database write happens unconditionally.
    """
    import re

    # Simple regex to extract task from common request patterns
    patterns = [
        r'add\s+(?:a\s+|an\s+)?(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
        r'create\s+(?:a\s+|an\s+)?(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
        r'new\s+(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
        r'add\s+"?([^"]+?)"?\s+(?:as\s+a\s+)?task',
        r'create\s+"?([^"]+?)"?\s+(?:as\s+a\s+)?task',
        r'add\s+(?!a\s|an\s)([^,.!?]+?)(?:\s|$)',  # Last resort: anything after "add"
    ]

    task_title = None
    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            task_title = match.group(1).strip()
            if task_title:
                task_title = task_title.replace('to ', '', 1) if task_title.startswith('to ') else task_title
                task_title = task_title.capitalize()
                break

    # If we couldn't extract a title from patterns, use the first part of the message
    if not task_title or len(task_title.strip()) < 2:
        # Take the first 50 characters as the title, or up to the first punctuation
        parts = re.split(r'[.!?]', message.strip(), 1)
        task_title = parts[0].strip()[:50].capitalize()

        # If it's still too short, use the whole message
        if len(task_title) < 2:
            task_title = message.strip()[:50].capitalize()

    if task_title and task_title.strip():
        # Create task service and save the task to database
        task_service = TaskService(session)
        from ...models.task import TaskCreate

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
    else:
        return "Could not extract task from request, but AI processing attempted."


# Actually connect to the AI agent
@router.post("/process_real", response_model=ChatResponse)
def process_chat_real(
    request: ChatRequest,
    current_user_id: UUID = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Process natural language requests using the AI agent.
    This endpoint connects the frontend to the AI agent for task management.
    """
    try:
        # Import the TodoAgent if available
        # First, check if OPENAI_API_KEY is available
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            # Even if API key is not available, try to create the task directly
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=f"{response} (AI functionality unavailable - missing OPENAI_API_KEY)")

        try:
            import subprocess
            import sys

            # Try to import the agent directly using the full path
            # Get the project root directory (two levels up from this file)
            current_dir = os.path.dirname(__file__)
            project_root = os.path.abspath(os.path.join(current_dir, "..", "..", "..", ".."))
            agent_src_path = os.path.join(project_root, "agent", "src")

            # Add the agent src path to sys.path
            original_path = sys.path[:]
            if agent_src_path not in sys.path:
                sys.path.insert(0, agent_src_path)

            try:
                # Import the TodoAgent
                from agents.todo_agent import TodoAgent

                # Initialize the agent
                agent = TodoAgent()

                # Process the request with the agent
                response = agent.process_request(request.message, str(current_user_id))

                return ChatResponse(response=response)
            finally:
                # Restore original path
                sys.path[:] = original_path
        except ImportError as e:
            print(f"Import error: {e}")
            # Even if agent is not available, ensure task creation happens
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=response)
        except Exception as e:
            print(f"AI agent error: {e}")
            # Check if it's an OpenAI API error with quota issues
            error_msg = str(e)
            if "insufficient_quota" in error_msg.lower() or "429" in error_msg:
                # Even if AI fails, try to create the task directly
                response = create_basic_task_from_request(request.message, current_user_id, session)
                return ChatResponse(response=f"{response} (AI enhancement unavailable due to quota limits)")
            else:
                # Even if AI fails, try to create the task directly
                response = create_basic_task_from_request(request.message, current_user_id, session)
                return ChatResponse(response=f"{response} (AI enhancement unavailable: {str(e)})")
    except Exception as e:
        print(f"General error: {e}")
        # Fallback: create basic task even if everything else fails
        try:
            response = create_basic_task_from_request(request.message, current_user_id, session)
            return ChatResponse(response=f"{response} (Processing error occurred: {str(e)})")
        except Exception as db_error:
            raise HTTPException(status_code=500, detail=f"Error processing chat request and creating task: {str(db_error)}")