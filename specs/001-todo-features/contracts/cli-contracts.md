# API Contracts: Todo Console App

## Task Management Operations

### Add Task
- **Command**: `add`
- **Input**: title (string, 1-100 chars), description (optional string, 0-500 chars)
- **Output**: Success message with task ID or error message
- **Errors**: 
  - "Error: Title is required and must be 1-100 characters" (if title invalid)
  - "Error: Title must be 1-100 characters" (if title too long)

### List Tasks
- **Command**: `list`
- **Input**: None
- **Output**: Formatted list of all tasks with ID, title, status, description and count summary
- **Errors**: "No tasks found" (if no tasks exist)

### Update Task
- **Command**: `update`
- **Input**: task ID (integer), new title (string, 1-100 chars), new description (optional string, 0-500 chars)
- **Output**: Success message or error message
- **Errors**:
  - "Error: Task with ID [X] not found" (if ID invalid)
  - "Error: Title is required and must be 1-100 characters" (if title invalid)

### Delete Task
- **Command**: `delete`
- **Input**: task ID (integer)
- **Output**: Confirmation prompt, then success message or cancellation message
- **Errors**: "Error: Task with ID [X] not found" (if ID invalid)

### Mark Complete
- **Command**: `complete`
- **Input**: task ID (integer)
- **Output**: Success message indicating status change
- **Errors**: "Error: Task with ID [X] not found" (if ID invalid)

### Exit Application
- **Command**: `exit`
- **Input**: None
- **Output**: Application terminates gracefully