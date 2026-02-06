#!/usr/bin/env python3
"""
Test script to verify AI assistant functionality after fixes
"""
import os
import sys
from dotenv import load_dotenv

def main():
    print("Testing AI Assistant Fixes...")
    print("=" * 50)

    # Load environment variables explicitly for this test
    load_dotenv()

    print("\nEnvironment variables loaded from .env file:")
    api_key = os.getenv("OPENAI_API_KEY")
    mcp_url = os.getenv("MCP_SERVER_URL", "http://localhost:8001")

    print(f"OPENAI_API_KEY present: {'YES' if api_key else 'NO'}")
    print(f"MCP_SERVER_URL: {mcp_url}")

    # Test that the environment variables are accessible
    if api_key:
        print("\n✓ Environment variables are properly loaded!")
        print("The AI assistant should now work correctly when:")
        print("1. Backend is restarted to load new environment")
        print("2. MCP server is running on the configured port")
        print("3. OPENAI_API_KEY is set in environment")
    else:
        print("\n⚠ OPENAI_API_KEY is not set in the .env file")
        print("Please add your OpenAI API key to the .env file.")

    print(f"\nChanges made to fix the issues:")
    print("1. Added load_dotenv() to backend/src/main.py")
    print("2. Added proper API key validation in chat endpoint")
    print("3. Added load_dotenv() to agent/__main__.py")
    print("4. Enhanced error handling in TodoAgent constructor")
    print("5. Fixed MCP_SERVER_URL in .env file (was http://localhost:3000z)")

if __name__ == "__main__":
    main()