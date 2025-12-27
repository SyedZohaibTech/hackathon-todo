# Implementation Plan: Todo Console App

**Branch**: `001-todo-features` | **Date**: 2025-12-28 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-todo-features/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a console-based todo application with CRUD operations for tasks. The application will follow a simple architecture with a main loop handling user commands, a task manager for business logic, and in-memory storage. The system will provide commands for adding, listing, updating, deleting, and marking tasks as complete, with proper validation and user-friendly error handling.

### Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Main Loop     │───▶│  Task Manager    │───▶│  Data Store     │
│   (CLI)         │    │                  │    │  (dict)         │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Command        │    │  Business Logic  │    │  Task Objects   │
│  Routing        │    │  (CRUD ops)      │    │  (in-memory)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (no external packages)
**Storage**: In-memory dictionary (dict) for task storage
**Testing**: pytest for unit and integration tests
**Target Platform**: Cross-platform console application
**Project Type**: Single console application
**Performance Goals**: <100ms response time for all operations
**Constraints**: Must use only Python standard library, in-memory storage only, console interface only
**Scale/Scope**: Single-user application, up to 10,000 tasks in memory

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Clean Code**: Implementation will follow clean code principles with clear variable names and logical structure
- **Type Hints Mandatory**: All functions, methods, and variables will include appropriate type hints
- **User-Friendly Errors**: All error messages will be clear and actionable for end users
- **Test-First Development**: Tests will be written before implementation following TDD principles
- **PEP 8 Compliance**: Code will comply with PEP 8 style guidelines with max 88 char line length
- **Spec-Driven Development**: Implementation will follow the established specification exactly
- **Technology Stack**: Will use Python 3.13+ with only standard library modules
- **Code Standards**: All functions will include comprehensive docstrings following Google conventions
- **Error Handling**: All inputs will be validated and errors handled gracefully without crashes

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-features/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # Entry point, menu, command routing
├── task_manager.py      # TaskManager class, CRUD operations
├── models.py            # Task dataclass
├── display.py           # Console formatting
└── utils.py             # Input validation

tests/
├── unit/
│   ├── test_models.py
│   ├── test_task_manager.py
│   └── test_utils.py
├── integration/
│   └── test_cli_flow.py
└── contract/
    └── test_api_contracts.py

requirements.txt           # Empty file for dependency tracking
README.md                # Project documentation
```

## Module Breakdown

### src/main.py - Entry point, menu, command routing
- Contains the main application loop
- Handles user input and command parsing
- Routes commands to appropriate handlers
- Manages application lifecycle

### src/task_manager.py - TaskManager class, CRUD operations
- Implements the TaskManager class
- Contains all business logic for task operations
- Handles validation and error management
- Manages the in-memory storage

### src/models.py - Task dataclass
- Defines the Task dataclass with id, title, description, completed, created_at
- Includes validation methods for task fields
- Provides string representation for display

### src/display.py - Console formatting
- Handles all console output formatting
- Provides methods for displaying tasks in a readable format
- Formats error messages for user consumption

### src/utils.py - Input validation
- Contains validation functions for user input
- Provides utilities for parsing command arguments
- Handles input sanitization

## Function Signatures

### TaskManager Class
```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

class TaskManager:
    def __init__(self):
        """Initialize the task manager with empty storage."""
        self.storage: Dict[int, Task] = {}
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task with the given title and description.

        Args:
            title: Required title (1-100 characters)
            description: Optional description (0-500 characters)

        Returns:
            The created Task object

        Raises:
            ValueError: If title doesn't meet validation requirements
        """
        pass

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks in the storage.

        Returns:
            List of all Task objects
        """
        pass

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> bool:
        """Update an existing task with new values.

        Args:
            task_id: ID of the task to update
            title: New title (if provided)
            description: New description (if provided)

        Returns:
            True if task was updated, False if task not found
        """
        pass

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False if task not found
        """
        pass

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            True if task status was toggled, False if task not found
        """
        pass
```

## Implementation Order

### Phase 1: Core Data Model (Steps 1-4)
1. Create `src/models.py` with Task dataclass
2. Create `src/task_manager.py` with basic TaskManager structure
3. Implement TaskManager.add_task method
4. Implement TaskManager.get_all_tasks method

### Phase 2: Core Operations (Steps 5-10)
5. Implement TaskManager.update_task method
6. Implement TaskManager.delete_task method
7. Implement TaskManager.toggle_complete method
8. Create `src/utils.py` with validation functions
9. Create `src/display.py` with formatting functions
10. Add error handling to all TaskManager methods

### Phase 3: CLI Interface (Steps 11-16)
11. Create `src/main.py` with basic application structure
12. Implement command parsing for 'add' command
13. Implement command parsing for 'list' command
14. Implement command parsing for 'update' command
15. Implement command parsing for 'delete' command
16. Implement command parsing for 'complete' command

### Phase 4: User Experience (Steps 17-20)
17. Add confirmation prompts for delete operation
18. Implement error handling in CLI layer
19. Add 'exit' command and graceful shutdown
20. Final testing and integration

## Error Handling Strategy

### Where errors are caught:
- **Input layer** (`src/utils.py`): Validates user input before processing
- **Business logic layer** (`src/task_manager.py`): Handles domain-specific validation and operations
- **Presentation layer** (`src/main.py`): Catches and formats errors for user display

### How errors are handled:
- All validation errors are caught and converted to user-friendly messages
- Invalid operations (e.g., updating non-existent tasks) return appropriate boolean values
- Unexpected errors are caught and converted to graceful error messages
- The application never crashes, but always returns to a stable state

**Structure Decision**: Single console application structure selected based on requirements for a simple, single-user todo application with console interface only.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (None) | (None) | (None) |

## Data Structures

### Task Dataclass
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

storage: Dict[int, Task] = {}
```
