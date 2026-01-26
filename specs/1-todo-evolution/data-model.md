# Data Model: Hackathon II – Spec-Driven Evolution of Todo

## Core Entities

### Task
Represents a user's todo item with properties like title, description, completion status, creation date, and owner

**Fields:**
- `id`: UUID (Primary Key) - Unique identifier for the task
- `title`: String (Required, Max 255) - Title of the task
- `description`: Text (Optional) - Detailed description of the task
- `completed`: Boolean (Default: False) - Whether the task is completed
- `created_at`: DateTime (Auto-generated) - When the task was created
- `updated_at`: DateTime (Auto-generated) - When the task was last updated
- `due_date`: DateTime (Optional) - When the task is due
- `priority`: Integer (Default: 1, Range: 1-5) - Priority level (1=low, 5=high)
- `user_id`: UUID (Foreign Key) - Owner of the task

**Relationships:**
- Belongs to one User
- Can have many Comments (optional)

**Validation Rules:**
- Title must not be empty
- User_id must reference an existing user
- Due date cannot be in the past (optional validation)

### User
Represents an authenticated user with properties like user ID, authentication tokens, and associated tasks

**Fields:**
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String (Required, Unique, Email format) - User's email address
- `username`: String (Required, Unique, Max 50) - User's chosen username
- `hashed_password`: String (Required) - Hashed password for authentication
- `first_name`: String (Optional, Max 100) - User's first name
- `last_name`: String (Optional, Max 100) - User's last name
- `created_at`: DateTime (Auto-generated) - When the user account was created
- `updated_at`: DateTime (Auto-generated) - When the user account was last updated
- `is_active`: Boolean (Default: True) - Whether the account is active
- `last_login_at`: DateTime (Optional) - When the user last logged in

**Relationships:**
- Has many Tasks
- Has many Conversations (optional)

**Validation Rules:**
- Email must be in valid email format
- Username must be 3-50 characters and alphanumeric with underscores/hyphens
- Password must meet security requirements (handled by auth service)

### Conversation
Represents an AI chat session with properties like conversation ID, user context, and message history

**Fields:**
- `id`: UUID (Primary Key) - Unique identifier for the conversation
- `user_id`: UUID (Foreign Key) - User who owns the conversation
- `title`: String (Optional, Max 255) - Title of the conversation
- `created_at`: DateTime (Auto-generated) - When the conversation started
- `updated_at`: DateTime (Auto-generated) - When the conversation was last updated
- `is_active`: Boolean (Default: True) - Whether the conversation is ongoing
- `context_data`: JSON (Optional) - Additional context for the AI agent

**Relationships:**
- Belongs to one User
- Has many Messages (optional)

**Validation Rules:**
- User_id must reference an existing user
- Title is optional but if provided must not be empty

### Event
Represents a system event like task creation/update/deletion with properties like event type, timestamp, and payload

**Fields:**
- `id`: UUID (Primary Key) - Unique identifier for the event
- `event_type`: String (Required) - Type of event (task.created, task.updated, task.deleted, etc.)
- `payload`: JSON (Required) - Event data containing relevant information
- `timestamp`: DateTime (Auto-generated) - When the event occurred
- `user_id`: UUID (Optional) - User associated with the event
- `correlation_id`: UUID (Optional) - Links related events together
- `processed`: Boolean (Default: False) - Whether the event has been processed

**Relationships:**
- Optionally belongs to one User

**Validation Rules:**
- Event_type must be one of the predefined event types
- Payload must be valid JSON

## State Transitions

### Task State Transitions
- **Created**: When a new task is added to the system
- **Updated**: When any property of the task changes
- **Completed**: When the task status changes from incomplete to complete
- **Reopened**: When a completed task becomes incomplete again
- **Deleted**: When the task is removed from the system

### User State Transitions
- **Registered**: When a new user account is created
- **Activated**: When a user account becomes active
- **Deactivated**: When a user account is deactivated
- **LoggedIn**: When a user successfully authenticates
- **LoggedOut**: When a user ends their session

## Indexes

### Task Table
- Index on `user_id` for efficient user-specific queries
- Index on `completed` for filtering completed/incomplete tasks
- Index on `due_date` for sorting and querying by deadline
- Composite index on `(user_id, completed)` for combined filtering

### User Table
- Unique index on `email` for enforcing uniqueness
- Unique index on `username` for enforcing uniqueness
- Index on `is_active` for filtering active users

### Conversation Table
- Index on `user_id` for user-specific queries
- Index on `is_active` for filtering active conversations
- Index on `updated_at` for chronological ordering

### Event Table
- Index on `event_type` for filtering by event type
- Index on `user_id` for user-specific events
- Index on `timestamp` for chronological ordering
- Index on `processed` for tracking processed events

## Constraints

### Referential Integrity
- Foreign key constraint from Task.user_id to User.id
- Foreign key constraint from Conversation.user_id to User.id

### Data Integrity
- Task.title cannot be empty or null
- User.email and User.username must be unique
- Task.completed defaults to false
- User.is_active defaults to true

### Business Logic Constraints
- A task cannot be both completed and deleted simultaneously
- A user cannot access tasks owned by other users
- Events must have valid event_type values from predefined list