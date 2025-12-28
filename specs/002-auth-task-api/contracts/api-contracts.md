# API Contracts: Authentication and Task API

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Register a new user account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "Optional Name"
}
```

**Validation:**
- email: required, valid email format, unique
- password: required, minimum 8 characters
- name: optional, maximum 100 characters

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "message": "User created successfully"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

### POST /api/auth/login
**Description**: Authenticate user and return JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Validation:**
- email: required, valid email format
- password: required

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "token": "jwt_token_string",
    "user": {
      "id": "user-uuid",
      "email": "user@example.com",
      "name": "Optional Name"
    }
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Invalid credentials"
}
```

## Task Management Endpoints

### POST /api/{user_id}/tasks
**Description**: Create a new task for the specified user

**Headers:**
- Authorization: Bearer {jwt_token}

**Path Parameters:**
- user_id: UUID of the user (must match authenticated user)

**Request:**
```json
{
  "title": "Task title",
  "description": "Optional task description"
}
```

**Validation:**
- user_id: must match authenticated user
- title: required, 1-100 characters
- description: optional, max 500 characters

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Task title",
    "description": "Optional task description",
    "completed": false
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

### GET /api/{user_id}/tasks
**Description**: Retrieve all tasks for the specified user

**Headers:**
- Authorization: Bearer {jwt_token}

**Path Parameters:**
- user_id: UUID of the user (must match authenticated user)

**Response (Success):**
```json
{
  "success": true,
  "data": [
    {
      "id": 123,
      "user_id": "user-uuid",
      "title": "Task title",
      "description": "Optional task description",
      "completed": false
    }
  ]
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

### PUT /api/{user_id}/tasks/{id}
**Description**: Update an existing task

**Headers:**
- Authorization: Bearer {jwt_token}

**Path Parameters:**
- user_id: UUID of the user (must match authenticated user)
- id: Task ID to update

**Request:**
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Validation:**
- user_id: must match authenticated user
- id: must be a valid task ID belonging to the user
- title: required, 1-100 characters
- description: optional, max 500 characters

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Updated task title",
    "description": "Updated task description",
    "completed": false
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a task

**Headers:**
- Authorization: Bearer {jwt_token}

**Path Parameters:**
- user_id: UUID of the user (must match authenticated user)
- id: Task ID to delete

**Validation:**
- user_id: must match authenticated user
- id: must be a valid task ID belonging to the user

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "message": "Task deleted successfully"
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle the completion status of a task

**Headers:**
- Authorization: Bearer {jwt_token}

**Path Parameters:**
- user_id: UUID of the user (must match authenticated user)
- id: Task ID to update

**Validation:**
- user_id: must match authenticated user
- id: must be a valid task ID belonging to the user

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": 123,
    "user_id": "user-uuid",
    "title": "Task title",
    "description": "Optional task description",
    "completed": true
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error message"
}
```

## Error Response Format

All error responses follow this format:
```json
{
  "success": false,
  "error": "Descriptive error message"
}
```

## Success Response Format

All success responses follow this format:
```json
{
  "success": true,
  "data": { ... }
}
```