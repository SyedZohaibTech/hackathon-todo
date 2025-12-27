# Quickstart Guide: Todo Console App

## Prerequisites
- Python 3.13+ installed on your system

## Getting Started

1. Clone or download the repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   python src/main.py
   ```

## Available Commands

Once the application is running, you can use the following commands:

### Add a Task
```
add
```
You will be prompted to enter a title (required, 1-100 characters) and description (optional, up to 500 characters).

### List All Tasks
```
list
```
Displays all tasks with their ID, title, status (completed/incomplete), and description.

### Update a Task
```
update
```
You will be prompted to enter the task ID, new title, and new description.

### Delete a Task
```
delete
```
You will be prompted to enter the task ID. A confirmation prompt will appear before deletion.

### Mark Task as Complete/Incomplete
```
complete
```
You will be prompted to enter the task ID. This toggles the completion status of the task.

### Exit the Application
```
exit
```
Terminates the application gracefully.

## Example Usage

```
> add
Enter task title (1-100 characters): Buy groceries
Enter task description (optional, max 500 characters): Milk, bread, eggs
Task added successfully with ID: 1

> list
ID: 1 | Title: Buy groceries | Status: Incomplete | Description: Milk, bread, eggs
Total tasks: 1

> complete
Enter task ID: 1
Task 1 marked as complete

> list
ID: 1 | Title: Buy groceries | Status: Complete | Description: Milk, bread, eggs
Total tasks: 1

> exit
Goodbye!
```

## Error Handling

The application provides user-friendly error messages:

- If you enter an invalid command: "Error: Unknown command. Available commands: add, list, update, delete, complete, exit"
- If you enter an invalid task ID: "Error: Task with ID [X] not found"
- If you enter an invalid title: "Error: Title is required and must be 1-100 characters"
- If you enter a title that's too long: "Error: Title must be 1-100 characters"