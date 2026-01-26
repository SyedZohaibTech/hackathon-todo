# Quickstart Guide: Hackathon II – Spec-Driven Evolution of Todo

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ installed
- Docker and Docker Compose
- Kubernetes cluster (Minikube for local development)
- Git

## Initial Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
NEON_DATABASE_URL=postgresql://username:password@ep-...

# Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Agent Configuration
OPENAI_API_KEY=your-openai-api-key
AGENT_ID=todo-agent-id

# MCP Configuration
MCP_SERVER_URL=http://localhost:8000
MCP_API_KEY=your-mcp-api-key

# Dapr Configuration
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001
```

## Running the Application

### Phase I - Console Application
```bash
cd backend
python -m src.main console
```

### Phase II - Web Application Only
```bash
# Terminal 1: Start the backend
cd backend
python -m src.main api

# Terminal 2: Start the frontend
cd frontend
npm run dev
```

### Phase III - With AI Agent
```bash
# Terminal 1: Start the backend
cd backend
python -m src.main api

# Terminal 2: Start the MCP server
cd backend
python -m src.mcp_server.server

# Terminal 3: Start the AI agent
cd agent
python -m src.agents.todo_agent

# Terminal 4: Start the frontend
cd frontend
npm run dev
```

### Phase IV - Kubernetes Deployment
```bash
# Start Minikube
minikube start

# Deploy to Kubernetes
kubectl apply -f infra/k8s/manifests/

# Or use Helm
helm install todo-app infra/k8s/helm/ --values infra/k8s/helm/values.yaml
```

### Phase V - With Kafka and Event Processing
```bash
# Terminal 1: Start Kafka and Zookeeper
docker-compose -f infra/docker/kafka-docker-compose.yml up -d

# Terminal 2: Start backend with event processing
cd backend
python -m src.main api

# Terminal 3: Start event processors
cd backend
python -m src.services.event_processor

# Continue with other services as needed
```

## API Endpoints

### Task Management
- `GET /api/v1/tasks` - Get all tasks for authenticated user
- `POST /api/v1/tasks` - Create a new task
- `GET /api/v1/tasks/{task_id}` - Get a specific task
- `PUT /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task
- `PATCH /api/v1/tasks/{task_id}/complete` - Mark task as complete
- `PATCH /api/v1/tasks/{task_id}/incomplete` - Mark task as incomplete

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info

### User Management
- `GET /api/v1/users/me` - Get current user details
- `PUT /api/v1/users/me` - Update current user details
- `DELETE /api/v1/users/me` - Deactivate current user account

## MCP Tools Available

### Task Operations
- `create_task(title: str, description: str, due_date: str)` - Create a new task
- `get_tasks()` - Retrieve all user tasks
- `update_task(task_id: str, title: str, description: str, completed: bool)` - Update a task
- `delete_task(task_id: str)` - Delete a task
- `mark_task_completed(task_id: str)` - Mark a task as completed
- `mark_task_incomplete(task_id: str)` - Mark a task as incomplete

## Testing

### Unit Tests
```bash
# Backend tests
cd backend
pytest tests/unit/

# Frontend tests
cd frontend
npm run test
```

### Integration Tests
```bash
# Backend integration tests
cd backend
pytest tests/integration/

# End-to-end tests
cd frontend
npm run test:e2e
```

### Contract Tests
```bash
# API contract tests
cd backend
pytest tests/contract/
```

## Development Commands

### Generate Documentation
```bash
cd backend
python -m src.main docs
```

### Run Linters
```bash
# Backend
cd backend
flake8 src/
black --check src/

# Frontend
cd frontend
npm run lint
npm run format:check
```

### Database Migrations
```bash
cd backend
# Create migration
python -m alembic revision --autogenerate -m "migration message"

# Apply migration
python -m alembic upgrade head
```

## Docker Commands

### Build Images
```bash
# Build all services
docker-compose -f infra/docker/docker-compose.build.yml build

# Build individual services
docker build -t todo-backend -f infra/docker/backend.Dockerfile .
docker build -t todo-frontend -f infra/docker/frontend.Dockerfile .
docker build -t todo-agent -f infra/docker/agent.Dockerfile .
```

### Run with Docker
```bash
# Run all services
docker-compose -f infra/docker/docker-compose.dev.yml up

# Run in detached mode
docker-compose -f infra/docker/docker-compose.dev.yml up -d
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Ensure PostgreSQL is running and accessible
   - Verify DATABASE_URL in environment variables
   - Check database migrations are applied

2. **Authentication Problems**
   - Verify JWT_SECRET_KEY is set correctly
   - Ensure tokens aren't expired
   - Check user is active in the database

3. **AI Agent Not Responding**
   - Confirm MCP server is running
   - Verify OPENAI_API_KEY is set
   - Check network connectivity between services

4. **Kubernetes Deployment Failures**
   - Ensure Minikube is running
   - Verify all required secrets are created
   - Check resource limits aren't exceeded

### Useful Commands

```bash
# Check backend health
curl http://localhost:8000/health

# Check database connection
python -c "import sqlalchemy; engine = sqlalchemy.create_engine('your-db-url'); engine.connect()"

# View logs
kubectl logs -f deployment/todo-backend
```