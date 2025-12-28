# Quickstart Guide: Authentication and Task API

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.13+ for backend development
- PostgreSQL database (Neon recommended)
- Git for version control

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hackathon-todo
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend/

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL, JWT secret, etc.
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend/

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API URL and other variables
```

### 4. Database Setup
```bash
# In the backend directory
cd backend/

# Run database migrations
python -m alembic upgrade head
```

## Running the Application

### Backend (FastAPI)
```bash
cd backend/
python main.py
# or
uvicorn main:app --reload
```

### Frontend (Next.js)
```bash
cd frontend/
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/login` - Authenticate and get JWT token

### Task Management
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/dbname
JWT_SECRET=your_jwt_secret_key
FRONTEND_URL=http://localhost:3000
```

### Frontend (.env)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your_auth_secret
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Testing

### Backend Tests
```bash
cd backend/
pytest
```

### Frontend Tests
```bash
cd frontend/
npm test
```

## Deployment

### Backend
The backend can be deployed to any Python-compatible hosting service. Ensure environment variables are properly configured.

### Frontend
The frontend is built with Next.js and can be deployed to Vercel (as specified in the constitution) or any other hosting service that supports Next.js applications.