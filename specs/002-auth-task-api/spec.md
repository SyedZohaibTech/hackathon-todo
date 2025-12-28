# Feature Specification: Authentication and Task API

**Feature Branch**: `002-auth-task-api`
**Created**: 2025-12-28
**Status**: Draft
**Input**: User description: "Based on @specs/phase2/constitution.md, specify Phase II features. **Feature 1: Authentication** - Signup: email (valid), password (8+ chars), name (optional) - Login: email + password → JWT token (7 days) - Logout: clear token, redirect - Protected routes require valid JWT **Feature 2: REST API (5 CRUD endpoints)** ``` POST /api/{user_id}/tasks # Create GET /api/{user_id}/tasks # List (user's only) PUT /api/{user_id}/tasks/{id} # Update DELETE /api/{user_id}/tasks/{id} # Delete PATCH /api/{user_id}/tasks/{id}/complete # Toggle ``` - All require JWT in Authorization header - User can only access own tasks (verify user_id) **Feature 3: Web UI** - Pages: /login, /signup, / (dashboard - protected) - Components: LoginForm, SignupForm, TaskList, TaskItem, TaskForm - Mobile responsive (375px+) - Loading states + error messages **Data Models:** ```typescript User: { id: UUID, email: string, name?: string, password_hash: string } Task: { id: int, user_id: UUID, title: string(1-100), description?: string(max 500), completed: bool } ``` **API Response:** ```json Success: {"success": true, "data": {...}} Error: {"success": false, "error": "message"} ``` **Validation:** - Email: valid format, unique - Password: min 8 chars - Title: 1-100 chars required - Description: max 500 chars optional **Edge Cases:** - Empty list: "No tasks yet" - Token expired: auto-logout - Invalid credentials: clear error - Unauthorized access: 403"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

A new user wants to create an account in the todo application to start managing their tasks. They need to provide their email, password, and optionally their name to register.

**Why this priority**: This is the foundational step that allows new users to access the system and is required before they can use any other features.

**Independent Test**: A new user can navigate to the signup page, enter valid credentials (email, password of 8+ chars, optional name), submit the form, and successfully create an account with appropriate feedback.

**Acceptance Scenarios**:

1. **Given** a user is on the signup page, **When** they enter valid email, password (8+ chars), and optional name, **Then** their account is created and they are redirected to login page with success message
2. **Given** a user enters invalid email format, **When** they submit the form, **Then** they see an error message indicating invalid email format
3. **Given** a user enters password with less than 8 characters, **When** they submit the form, **Then** they see an error message indicating minimum password length

---

### User Story 2 - User Authentication (Priority: P1)

An existing user wants to log into the todo application to access their tasks. They need to provide their email and password to authenticate and receive a JWT token.

**Why this priority**: This is the entry point for existing users to access their data and is required for all protected functionality.

**Independent Test**: An existing user can navigate to the login page, enter valid credentials (email and password), and successfully authenticate to receive a JWT token and access to their dashboard.

**Acceptance Scenarios**:

1. **Given** a user is on the login page, **When** they enter valid email and password, **Then** they receive a JWT token and are redirected to the dashboard
2. **Given** a user enters invalid credentials, **When** they submit the form, **Then** they see an error message indicating invalid credentials
3. **Given** a user's JWT token expires after 7 days, **When** they try to access protected routes, **Then** they are redirected to the login page

---

### User Story 3 - Task Management (Priority: P1)

An authenticated user wants to manage their tasks by creating, viewing, updating, and deleting them. They should only see tasks that belong to them.

**Why this priority**: This is the core functionality of the todo application that provides value to users.

**Independent Test**: An authenticated user can create, view, update, and delete their tasks through the web interface, with all operations properly authenticated and authorized.

**Acceptance Scenarios**:

1. **Given** an authenticated user is on the dashboard, **When** they create a new task with valid title (1-100 chars) and optional description, **Then** the task is saved and appears in their task list
2. **Given** an authenticated user has tasks, **When** they view their dashboard, **Then** they see only their own tasks
3. **Given** an authenticated user wants to update a task, **When** they modify task details and save, **Then** the task is updated in the system
4. **Given** an authenticated user wants to delete a task, **When** they confirm deletion, **Then** the task is removed from their list

---

### User Story 4 - Task Completion Toggle (Priority: P2)

An authenticated user wants to mark tasks as complete or incomplete to track their progress. This should be a simple toggle operation.

**Why this priority**: This provides a quick way for users to update task status without navigating to edit forms.

**Independent Test**: An authenticated user can toggle the completion status of their tasks with a single action, and the change is reflected immediately in the UI and persisted in the system.

**Acceptance Scenarios**:

1. **Given** an authenticated user has tasks, **When** they click the completion toggle for a task, **Then** the task's completion status is updated and reflected in the UI
2. **Given** an authenticated user has a completed task, **When** they click the completion toggle, **Then** the task is marked as incomplete

---

### User Story 5 - Protected Routes (Priority: P2)

Users should only be able to access protected pages when they have a valid JWT token. If the token is missing or expired, they should be redirected to the login page.

**Why this priority**: This is critical for security to ensure that only authenticated users can access sensitive functionality.

**Independent Test**: When a user attempts to access a protected route without a valid JWT token, they are redirected to the login page with an appropriate message.

**Acceptance Scenarios**:

1. **Given** a user without a valid JWT token, **When** they try to access the dashboard, **Then** they are redirected to the login page
2. **Given** a user with an expired JWT token, **When** they try to access any protected route, **Then** they are redirected to the login page

---

### Edge Cases

- What happens when a user tries to access another user's tasks? The system should return a 403 Forbidden error.
- How does the system handle an empty task list? The UI should display "No tasks yet" message.
- What happens when a JWT token expires during a session? The system should detect this and redirect to the login page with an appropriate message.
- How does the system handle invalid credentials during login? The system should return a clear error message without revealing whether the email or password was incorrect.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to register with a valid email address, password (minimum 8 characters), and optional name
- **FR-002**: System MUST validate email format according to standard email validation rules
- **FR-003**: System MUST ensure email addresses are unique across all users
- **FR-004**: System MUST hash passwords using bcrypt before storing them
- **FR-005**: System MUST authenticate users via email and password, issuing a JWT token valid for 7 days upon successful login
- **FR-006**: System MUST provide a logout function that clears the JWT token and redirects the user
- **FR-007**: System MUST protect all task-related routes requiring a valid JWT token
- **FR-008**: System MUST allow authenticated users to create tasks with a title (1-100 characters) and optional description (max 500 characters)
- **FR-009**: System MUST allow authenticated users to retrieve only their own tasks
- **FR-010**: System MUST allow authenticated users to update their tasks
- **FR-011**: System MUST allow authenticated users to delete their tasks
- **FR-012**: System MUST allow authenticated users to toggle the completion status of their tasks
- **FR-013**: System MUST return standardized API responses with success/error status and data/error message
- **FR-014**: System MUST implement proper error handling and return user-friendly error messages
- **FR-015**: System MUST implement mobile-responsive UI that works on screens down to 375px width
- **FR-016**: System MUST display appropriate loading states during API operations
- **FR-017**: System MUST handle token expiration by redirecting to login page automatically

### Key Entities *(include if feature involves data)*

- **User**: Represents a registered user with an email, optional name, and password hash
- **Task**: Represents a todo item with a title, optional description, and completion status, associated with a specific user

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration with valid credentials in under 30 seconds
- **SC-002**: Users can log in with valid credentials and receive JWT token in under 10 seconds
- **SC-003**: 95% of users successfully complete the registration process without errors
- **SC-004**: Users can create a new task in under 15 seconds from the dashboard
- **SC-005**: Users can view their task list in under 5 seconds after authentication
- **SC-006**: 99% of task operations (create, read, update, delete) complete successfully
- **SC-007**: The system correctly prevents unauthorized access to other users' tasks 100% of the time
- **SC-008**: The UI is fully responsive and usable on screen sizes down to 375px
- **SC-009**: 90% of users can successfully log out and have their session cleared
- **SC-010**: Users can toggle task completion status with a response time under 3 seconds