---
id: 001
title: Auth Task API Spec
stage: spec
date_iso: 2025-12-28
model: Qwen
feature: auth-task-api
branch: 002-auth-task-api
user: user
command: /sp.specify
labels: ["authentication", "api", "task-management", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/002-auth-task-api/spec.md"
  - "specs/002-auth-task-api/checklists/requirements.md"
tests_yaml: []
prompt_text: |
  Based on @specs/phase2/constitution.md, specify Phase II features. **Feature 1: Authentication** - Signup: email (valid), password (8+ chars), name (optional) - Login: email + password → JWT token (7 days) - Logout: clear token, redirect - Protected routes require valid JWT **Feature 2: REST API (5 CRUD endpoints)** ``` POST /api/{user_id}/tasks # Create GET /api/{user_id}/tasks # List (user's only) PUT /api/{user_id}/tasks/{id} # Update DELETE /api/{user_id}/tasks/{id} # Delete PATCH /api/{user_id}/tasks/{id}/complete # Toggle ``` - All require JWT in Authorization header - User can only access own tasks (verify user_id) **Feature 3: Web UI** - Pages: /login, /signup, / (dashboard - protected) - Components: LoginForm, SignupForm, TaskList, TaskItem, TaskForm - Mobile responsive (375px+) - Loading states + error messages **Data Models:** ```typescript User: { id: UUID, email: string, name?: string, password_hash: string } Task: { id: int, user_id: UUID, title: string(1-100), description?: string(max 500), completed: bool } ``` **API Response:** ```json Success: {"success": true, "data": {...}} Error: {"success": false, "error": "message"} ``` **Validation:** - Email: valid format, unique - Password: min 8 chars - Title: 1-100 chars required - Description: max 500 chars optional **Edge Cases:** - Empty list: "No tasks yet" - Token expired: auto-logout - Invalid credentials: clear error - Unauthorized access: 403
response_text: |
  Successfully created the feature specification for authentication and task API. The specification includes:
  
  1. User stories for registration, authentication, task management, and protected routes
  2. Functional requirements covering user registration, authentication, task CRUD operations, and security
  3. Success criteria with measurable outcomes
  4. Key entities (User and Task)
  5. Edge cases handling
  
  The specification follows the constitution requirements and is ready for the planning phase.
outcome: |
  The feature specification for authentication and task API has been created at specs/002-auth-task-api/spec.md. The specification covers all required functionality including user authentication, task management API endpoints, and web UI components. A quality checklist was also created to validate the specification.
evaluation: |
  The specification is comprehensive and covers all the required functionality from the user description. It includes user stories, functional requirements, success criteria, and handles edge cases. The specification is ready for the planning phase.
---

# Auth Task API Spec

This PHR documents the creation of the feature specification for authentication and task API functionality.