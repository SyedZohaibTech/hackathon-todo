"""
Module: main.py
References: Task T008, T009, Spec §User Story 1
"""
from task_manager import TaskManager
from display import format_error_message, format_tasks_list
from utils import validate_title, validate_description, validate_task_id


def handle_add_task(task_manager: TaskManager, title: str, description: str = "") -> str:
    """Create the command handler for adding tasks.

    Args:
        task_manager: The TaskManager instance to use
        title: The title of the task to add
        description: The optional description of the task to add

    Returns:
        Success or error message
    """
    # Validate inputs
    if not validate_title(title):
        return format_error_message("Title is required and must be 1-100 characters")

    if not validate_description(description):
        return format_error_message("Description must be 0-500 characters")

    try:
        # Call TaskManager.add_task method
        task = task_manager.add_task(title, description)
        return f"Task added successfully with ID: {task.id}"
    except ValueError as e:
        return format_error_message(str(e))


def handle_list_tasks(task_manager: TaskManager) -> str:
    """Create the command handler for listing all tasks.

    Args:
        task_manager: The TaskManager instance to use

    Returns:
        Formatted list of tasks or error message
    """
    try:
        # Get all tasks from TaskManager
        tasks = task_manager.get_all_tasks()

        # Format and return the tasks list
        return format_tasks_list(tasks)
    except Exception as e:
        return format_error_message(f"Error retrieving tasks: {str(e)}")


def handle_update_task(task_manager: TaskManager, task_id: str, title: str = None, description: str = None) -> str:
    """Create the command handler for updating tasks.

    Args:
        task_manager: The TaskManager instance to use
        task_id: The ID of the task to update
        title: The new title (optional)
        description: The new description (optional)

    Returns:
        Success or error message
    """
    # Validate task_id
    if not validate_task_id(task_id):
        return format_error_message("Task ID must be a positive integer")

    # Convert task_id to integer
    task_id_int = int(task_id)

    # Validate title if provided
    if title is not None and not validate_title(title):
        return format_error_message("Title is required and must be 1-100 characters")

    # Validate description if provided
    if description is not None and not validate_description(description):
        return format_error_message("Description must be 0-500 characters")

    try:
        # Call TaskManager.update_task method
        success = task_manager.update_task(task_id_int, title, description)

        if success:
            return f"Task {task_id_int} updated successfully"
        else:
            return format_error_message(f"Task with ID {task_id_int} not found")
    except ValueError as e:
        return format_error_message(str(e))
    except Exception as e:
        return format_error_message(f"Error updating task: {str(e)}")


def handle_delete_task(task_manager: TaskManager, task_id: str) -> str:
    """Create the command handler for deleting tasks.

    Args:
        task_manager: The TaskManager instance to use
        task_id: The ID of the task to delete

    Returns:
        Success or error message
    """
    # Validate task_id
    if not validate_task_id(task_id):
        return format_error_message("Task ID must be a positive integer")

    # Convert task_id to integer
    task_id_int = int(task_id)

    try:
        # Call TaskManager.delete_task method
        success = task_manager.delete_task(task_id_int)

        if success:
            return f"Task {task_id_int} deleted successfully"
        else:
            return format_error_message(f"Task with ID {task_id_int} not found")
    except Exception as e:
        return format_error_message(f"Error deleting task: {str(e)}")


def handle_complete_task(task_manager: TaskManager, task_id: str) -> str:
    """Create the command handler for marking tasks complete.

    Args:
        task_manager: The TaskManager instance to use
        task_id: The ID of the task to toggle completion status

    Returns:
        Success or error message
    """
    # Validate task_id
    if not validate_task_id(task_id):
        return format_error_message("Task ID must be a positive integer")

    # Convert task_id to integer
    task_id_int = int(task_id)

    try:
        # Call TaskManager.toggle_complete method
        success = task_manager.toggle_complete(task_id_int)

        if success:
            # Get the task to check its new status
            task = task_manager.storage[task_id_int]
            status = "complete" if task.completed else "incomplete"
            return f"Task {task_id_int} marked as {status}"
        else:
            return format_error_message(f"Task with ID {task_id_int} not found")
    except Exception as e:
        return format_error_message(f"Error toggling task completion: {str(e)}")


def main():
    """Main application loop that handles user commands."""
    print("Welcome to the Todo Console App!")
    print("Available commands: add, list, update, delete, complete, exit")

    task_manager = TaskManager()

    while True:
        try:
            # Prompt for user input
            user_input = input("\nEnter command: ").strip()

            if not user_input:
                print(format_error_message("Please enter a command"))
                continue

            # Parse command and arguments
            parts = user_input.split(" ", 1)
            command = parts[0].lower()

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "add":
                # Handle the add command with direct input in the command line
                if len(parts) > 1:
                    # If arguments are provided after 'add'
                    args = parts[1].split(" | ", 1)  # Using " | " as separator between title and description
                    title = args[0].strip()
                    description = args[1].strip() if len(args) > 1 else ""
                else:
                    # If no arguments provided, prompt for them
                    print("Add command - please enter title and description")
                    title = input("Title: ").strip()
                    description = input("Description (optional): ").strip()

                result = handle_add_task(task_manager, title, description)
                print(result)
            elif command == "list":
                result = handle_list_tasks(task_manager)
                print(result)
            elif command == "update":
                # Handle the update command
                if len(parts) > 1:
                    # Parse arguments: task_id title | description
                    args = parts[1].split(" | ", 1)
                    task_id_and_title = args[0].split(" ", 1)

                    if len(task_id_and_title) < 2:
                        print(format_error_message("Usage: update <task_id> <new_title> | <new_description>"))
                        continue

                    task_id = task_id_and_title[0]
                    title = task_id_and_title[1]
                    description = args[1].strip() if len(args) > 1 else None
                else:
                    # If no arguments provided, prompt for them
                    print("Update command - please enter task ID, new title, and new description")
                    task_id = input("Task ID: ").strip()
                    title = input("New title (optional): ").strip() or None
                    description = input("New description (optional): ").strip() or None

                result = handle_update_task(task_manager, task_id, title, description)
                print(result)
            elif command == "delete":
                # Handle the delete command
                if len(parts) > 1:
                    task_id = parts[1].strip()
                else:
                    # If no arguments provided, prompt for them
                    task_id = input("Task ID to delete: ").strip()

                # Validate task_id
                if not validate_task_id(task_id):
                    print(format_error_message("Task ID must be a positive integer"))
                    continue

                # Confirmation prompt
                confirm = input(f"Are you sure you want to delete task {task_id}? (yes/no): ").strip().lower()
                if confirm not in ['yes', 'y']:
                    print("Task deletion cancelled.")
                    continue

                result = handle_delete_task(task_manager, task_id)
                print(result)
            elif command == "complete":
                # Handle the complete command
                if len(parts) > 1:
                    task_id = parts[1].strip()
                else:
                    # If no arguments provided, prompt for them
                    task_id = input("Task ID to mark complete/incomplete: ").strip()

                # Validate task_id
                if not validate_task_id(task_id):
                    print(format_error_message("Task ID must be a positive integer"))
                    continue

                result = handle_complete_task(task_manager, task_id)
                print(result)
            else:
                print(format_error_message("Unknown command. Available commands: add, list, update, delete, complete, exit"))

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except ValueError as ve:
            print(format_error_message(f"Value error: {str(ve)}"))
        except KeyError as ke:
            print(format_error_message(f"Key error: {str(ke)}"))
        except Exception as e:
            print(format_error_message(f"An unexpected error occurred: {str(e)}"))


if __name__ == "__main__":
    main()