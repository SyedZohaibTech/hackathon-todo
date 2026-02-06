#!/usr/bin/env python3
"""
Test script to verify AI assistant functionality
"""
import os
import sys
import json
from uuid import UUID

def test_agent_import():
    """Test if the agent can be imported successfully"""
    # Add the agent src to the path
    agent_src_path = os.path.join(os.path.dirname(__file__), "agent", "src")
    sys.path.insert(0, agent_src_path)

    try:
        from agents.todo_agent import TodoAgent
        print("OK - Agent import successful")
        return True
    except ImportError as e:
        print(f"FAIL - Agent import failed: {e}")
        return False

def test_agent_initialization():
    """Test if the agent can be initialized successfully"""
    try:
        from agents.todo_agent import TodoAgent
        # Check if OPENAI_API_KEY is set
        if not os.getenv("OPENAI_API_KEY"):
            print("WARN - OPENAI_API_KEY not set in environment")
            return False

        agent = TodoAgent()
        print("OK - Agent initialization successful")
        return True
    except Exception as e:
        print(f"FAIL - Agent initialization failed: {e}")
        return False

def test_mcp_client_connection():
    """Test if the MCP client can connect to the server"""
    try:
        # Need to add tools to path separately
        tools_path = os.path.join(os.path.dirname(__file__), "agent", "src", "tools")
        sys.path.insert(0, tools_path)

        from mcp_client import MCPClient
        mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001")
        client = MCPClient(base_url=mcp_url)

        # Test connection by trying to get tasks for a dummy user
        result = client.get_tasks(user_id="dummy-user-id")
        print(f"OK - MCP client connection test completed (success: {result.success})")
        return True
    except Exception as e:
        print(f"FAIL - MCP client connection failed: {e}")
        return False

def main():
    print("Testing AI Assistant Integration...")
    print("=" * 50)

    # Test 1: Agent import
    if not test_agent_import():
        print("\nCannot proceed - agent import failed")
        return

    # Test 2: Agent initialization
    if not test_agent_initialization():
        print("\nCannot proceed - agent initialization failed")
        return

    # Test 3: MCP client connection
    test_mcp_client_connection()

    print("\n" + "=" * 50)
    print("Integration tests completed!")
    print("\nTo run the full system:")
    print("1. Make sure OPENAI_API_KEY is set in your environment")
    print("2. Start the MCP server: python -m agent")
    print("3. Start the main API: python backend/app.py")
    print("4. Access the chat interface at http://localhost:3000/chat")

if __name__ == "__main__":
    main()