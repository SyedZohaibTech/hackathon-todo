# Data Model: Todo Console App

## Task Entity

### Definition
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

### Fields
- **id**: Unique identifier for the task (integer)
- **title**: Required title with 1-100 characters
- **description**: Optional description with 0-500 characters
- **completed**: Boolean indicating completion status
- **created_at**: Timestamp of when the task was created

### Validation Rules
- `id`: Must be a unique positive integer
- `title`: Required field, 1-100 characters, cannot be empty or whitespace-only
- `description`: Optional field, 0-500 characters
- `completed`: Boolean value, defaults to False
- `created_at`: Automatically set when task is created

## Task Storage

### Definition
```python
from typing import Dict
storage: Dict[int, Task] = {}
```

### Structure
- Dictionary with task ID as key and Task object as value
- Provides O(1) lookup time for tasks by ID
- In-memory only, no persistence

### Operations
- Add task: `storage[task.id] = task`
- Get task: `storage[task_id]`
- Update task: `storage[task_id] = updated_task`
- Delete task: `del storage[task_id]`
- List all tasks: `list(storage.values())`

## State Transitions

### Task Completion
- Initial state: `completed = False`
- After toggle: `completed = True`
- After second toggle: `completed = False`

### Task Modification
- Title and description can be modified via update operation
- ID and creation timestamp remain immutable after creation