"""
Todo Agent for managing tasks via natural language
Uses OpenAI Agents SDK to interpret user intent and perform task operations
"""
import os
import requests
from openai import OpenAI
from openai import APIError, RateLimitError
from typing import Dict, Any, List
from pydantic import BaseModel
from ..tools.mcp_client import MCPClient


class TaskOperationResult(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] = {}


class TodoAgent:
    def __init__(self):
        # Get the OpenAI API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            # Don't raise an error - AI is optional, tasks can still be created
            self.client = None
        else:
            # Initialize OpenAI client
            self.client = OpenAI(api_key=api_key)

        # Initialize MCP client for task operations
        self.mcp_client = MCPClient(base_url=os.getenv("MCP_SERVER_URL", "http://localhost:8001"))

        # Define the agent's system prompt
        self.system_prompt = """
        You are a helpful Todo assistant. You can help users manage their tasks by creating,
        updating, completing, or deleting tasks. You should interpret the user's natural
        language requests and convert them into appropriate task operations.

        When the user gives a request:
        1. Identify the intent (create, update, complete, delete, list tasks)
        2. Extract relevant information (task title, description, etc.)
        3. Use the appropriate tool to perform the operation

        Always respond in a friendly, helpful tone.
        """

    def process_request(self, user_input: str, user_id: str) -> str:
        """
        Process a natural language request from a user and perform the appropriate task operation.

        Args:
            user_input: Natural language request from the user
            user_id: ID of the user making the request

        Returns:
            Response string to send back to the user
        """
        # First, determine the intent and extract parameters using a simple parser
        # This ensures we can at least create the task even if AI fails
        intent, params = self.parse_intent(user_input)

        # If it's a create task request, create the task in the database first
        if intent == "create_task" and "title" in params:
            # Create task directly in database first to guarantee persistence
            result = self.mcp_client.create_task(
                title=params.get("title", ""),
                description=params.get("description", ""),
                user_id=user_id,
                priority=params.get("priority", 1)
            )

            if result.success:
                # Task successfully created in database
                # Now try to enhance with AI if available
                if self.client:
                    try:
                        # Use AI for enhanced response generation
                        response = self.client.chat.completions.create(
                            model="gpt-4o-mini",  # Using gpt-4o-mini as replacement for gpt-4-turbo
                            messages=[
                                {"role": "system", "content": self.system_prompt},
                                {"role": "user", "content": user_input}
                            ]
                        )

                        ai_content = response.choices[0].message.content or ""
                        if ai_content.strip():
                            return f"{result.message} {ai_content}"
                        else:
                            return result.message

                    except RateLimitError:
                        # AI failed but task was created, return success with friendly message
                        return f"{result.message} (AI enhancement unavailable due to high demand)"
                    except APIError as e:
                        if "insufficient_quota" in str(e).lower():
                            return f"{result.message} (AI enhancement unavailable due to quota limits)"
                        else:
                            return f"{result.message} (AI enhancement unavailable: {str(e)})"
                    except Exception:
                        # AI failed but task was created, return success message
                        return result.message
                else:
                    # No AI available, just return the success message
                    return result.message
            else:
                # Task creation failed, return error
                return f"Failed to create task: {result.message}"
        else:
            # For other operations or if we couldn't parse a create request, use AI if available
            if self.client:
                try:
                    # Create a conversation with the OpenAI API
                    response = self.client.chat.completions.create(
                        model="gpt-4o-mini",  # Using gpt-4o-mini as replacement for gpt-4-turbo
                        messages=[
                            {"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        functions=[
                            {
                                "name": "create_task",
                                "description": "Create a new task",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string", "description": "Title of the task"},
                                        "description": {"type": "string", "description": "Description of the task"},
                                        "priority": {"type": "integer", "description": "Priority level (1-5)", "default": 1}
                                    },
                                    "required": ["title"]
                                }
                            },
                            {
                                "name": "get_tasks",
                                "description": "Get all tasks for the user"
                            },
                            {
                                "name": "update_task",
                                "description": "Update an existing task",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to update"},
                                        "title": {"type": "string", "description": "New title of the task"},
                                        "description": {"type": "string", "description": "New description of the task"},
                                        "completed": {"type": "boolean", "description": "Whether the task is completed"}
                                    }
                                }
                            },
                            {
                                "name": "delete_task",
                                "description": "Delete a task",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to delete"}
                                    },
                                    "required": ["task_id"]
                                }
                            },
                            {
                                "name": "mark_task_completed",
                                "description": "Mark a task as completed",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to mark as completed"}
                                    },
                                    "required": ["task_id"]
                                }
                            },
                            {
                                "name": "mark_task_incomplete",
                                "description": "Mark a task as incomplete",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "task_id": {"type": "string", "description": "ID of the task to mark as incomplete"}
                                    },
                                    "required": ["task_id"]
                                }
                            }
                        ],
                        function_call="auto"
                    )

                    # Check if the model wants to call a function
                    message = response.choices[0].message

                    if message.function_call:
                        # Extract function name and arguments
                        import json
                        function_name = message.function_call.name
                        function_args = json.loads(message.function_call.arguments)

                        # Call the appropriate function on the MCP client
                        if function_name == "create_task":
                            result = self.mcp_client.create_task(
                                title=function_args.get("title"),
                                description=function_args.get("description", ""),
                                user_id=user_id,
                                priority=function_args.get("priority", 1)
                            )
                        elif function_name == "get_tasks":
                            result = self.mcp_client.get_tasks(user_id=user_id)
                        elif function_name == "update_task":
                            result = self.mcp_client.update_task(
                                task_id=function_args.get("task_id"),
                                user_id=user_id,
                                title=function_args.get("title"),
                                description=function_args.get("description"),
                                completed=function_args.get("completed")
                            )
                        elif function_name == "delete_task":
                            result = self.mcp_client.delete_task(
                                task_id=function_args.get("task_id"),
                                user_id=user_id
                            )
                        elif function_name == "mark_task_completed":
                            result = self.mcp_client.mark_task_completed(
                                task_id=function_args.get("task_id"),
                                user_id=user_id
                            )
                        elif function_name == "mark_task_incomplete":
                            result = self.mcp_client.mark_task_incomplete(
                                task_id=function_args.get("task_id"),
                                user_id=user_id
                            )
                        else:
                            return f"Unknown function: {function_name}"

                        # Format the result for the AI to respond with
                        if result.success:
                            return result.message
                        else:
                            return f"Error performing operation: {result.message}"
                    else:
                        # If no function call was made, return the AI's response
                        return message.content or "I processed your request."

                except RateLimitError as e:
                    # Specifically handle rate limiting and quota errors
                    return "I'm currently experiencing high demand and unable to process your request. AI assistance is temporarily unavailable. Please try again later or use the standard task management features."
                except APIError as e:
                    # Handle other OpenAI API errors
                    error_msg = str(e)
                    if "insufficient_quota" in error_msg.lower():
                        return "I'm currently experiencing high demand and unable to process your request. AI assistance is temporarily unavailable. Please try again later or use the standard task management features."
                    else:
                        return f"Sorry, I encountered an error processing your request: {error_msg}"
                except Exception as e:
                    # Handle any other unexpected errors
                    return f"Sorry, I encountered an error processing your request: {str(e)}"
            else:
                # No AI available, return a message indicating that
                return "AI functionality is currently unavailable. Please use the standard task management features."

    def parse_intent(self, user_input: str) -> tuple[str, dict]:
        """
        Simple parser to extract intent and parameters from user input.
        This ensures we can at least create basic tasks without AI.
        """
        import re

        user_lower = user_input.lower().strip()

        # Patterns for task creation
        create_patterns = [
            r'add\s+(?:a\s+|an\s+)?(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
            r'create\s+(?:a\s+|an\s+)?(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
            r'new\s+(?:task|to-do|todo)\s+(?:to\s+|called\s+)?"?([^"]+?)"?(?:\s|$)',
            r'add\s+"?([^"]+?)"?\s+(?:as\s+a\s+)?task',
            r'create\s+"?([^"]+?)"?\s+(?:as\s+a\s+)?task',
            r'add\s+(?!a\s|an\s)([^,.!?]+?)(?:\s|$)',  # Last resort: anything after "add"
        ]

        for pattern in create_patterns:
            match = re.search(pattern, user_lower)
            if match:
                title = match.group(1).strip()
                if title:
                    # Clean up the title
                    title = title.replace('to ', '', 1) if title.startswith('to ') else title
                    return "create_task", {"title": title.capitalize()}

        # If no clear create intent, return generic
        return "unknown", {}

    def chat(self, messages: List[Dict[str, str]], user_id: str) -> str:
        """
        Process a conversation with multiple messages.

        Args:
            messages: List of messages in the conversation
            user_id: ID of the user

        Returns:
            Response string to send back to the user
        """
        # For simplicity, we'll just process the last message
        # In a real implementation, you'd want to maintain conversation context
        if messages:
            last_message = messages[-1]["content"]
            return self.process_request(last_message, user_id)
        return "Hello! How can I help you with your tasks today?"


if __name__ == "__main__":
    # Example usage
    agent = TodoAgent()

    # Example user request
    user_input = "Add a task to buy groceries"
    user_id = "test-user-123"

    response = agent.process_request(user_input, user_id)
    print(f"Response: {response}")