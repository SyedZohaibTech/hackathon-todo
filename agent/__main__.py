"""
Main entry point for the Todo Agent
"""
from .src.agents.todo_agent import TodoAgent

def main():
    print("Starting Todo Agent...")
    agent = TodoAgent()

    # For now, just run a simple test
    print("Todo Agent is ready to process requests.")

    # Example usage:
    # response = agent.process_request("Add a task to buy groceries", "test-user-123")
    # print(f"Response: {response}")

if __name__ == "__main__":
    main()