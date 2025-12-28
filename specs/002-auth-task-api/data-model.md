# Data Model: Authentication and Task API

## User Entity

**Fields:**
- `id`: UUID (Primary Key, auto-generated)
- `email`: string (Unique, required, valid email format)
- `name`: string (Optional, max 100 characters)
- `password_hash`: string (Required, hashed with bcrypt)

**Validation Rules:**
- Email must be a valid email format
- Email must be unique across all users
- Password must be at least 8 characters when provided (before hashing)
- Name is optional and limited to 100 characters if provided

**Relationships:**
- One-to-Many: User has many Tasks (via user_id foreign key)

## Task Entity

**Fields:**
- `id`: int (Primary Key, auto-increment)
- `user_id`: UUID (Foreign Key referencing User.id, required)
- `title`: string (Required, 1-100 characters)
- `description`: string (Optional, max 500 characters)
- `completed`: bool (Required, default: false)

**Validation Rules:**
- Title is required and must be between 1 and 100 characters
- Description is optional and limited to 500 characters if provided
- Completed field is required and defaults to false
- user_id must reference an existing User

**Relationships:**
- Many-to-One: Task belongs to one User (via user_id foreign key)

## State Transitions

### Task State Transitions:
- `incomplete` → `complete`: When user toggles task completion via PATCH /api/{user_id}/tasks/{id}/complete
- `complete` → `incomplete`: When user toggles task completion via PATCH /api/{user_id}/tasks/{id}/complete

## Database Constraints

- User.email: UNIQUE constraint to ensure no duplicate email addresses
- Task.user_id: FOREIGN KEY constraint referencing User.id with CASCADE delete
- Task.title: NOT NULL and length constraint (1-100 characters)
- Task.completed: NOT NULL with default value of false