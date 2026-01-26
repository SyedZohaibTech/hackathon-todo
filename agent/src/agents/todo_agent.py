"""
Todo Agent for managing tasks via natural language
Uses OpenAI Agents SDK to interpret user intent and perform task operations
"""
import os
from openai import OpenAI
from typing import Dict, Any, List
from pydantic import BaseModel
from ..tools.mcp_client import MCPClient


class TaskOperationResult(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any] = {}


class TodoAgent:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
        try:
            # Create a conversation with the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",  # Using gpt-4-turbo for better reasoning
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
                function_name = message.function_call.name
                function_args = eval(message.function_call.arguments)

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

        except Exception as e:
            return f"Sorry, I encountered an error processing your request: {str(e)}"

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