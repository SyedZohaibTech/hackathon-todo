# Implementation Plan: Hackathon II – Spec-Driven Evolution of Todo (AI-Native Cloud Application)

**Branch**: `1-todo-evolution` | **Date**: 2026-01-23 | **Spec**: specs/1-todo-evolution/spec.md
**Input**: Feature specification from `/specs/1-todo-evolution/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a multi-phase Todo application evolving from an in-memory console app to a distributed, cloud-native, AI-powered system. The system will demonstrate Spec-Driven Development, agentic AI development, MCP-based tool governance, and cloud-native architecture patterns. The implementation follows five distinct phases with increasing complexity: Foundation (console), Full-Stack Web, AI Agent Integration, Local Kubernetes Deployment, and Cloud-Native Event-Driven System.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI, SQLModel, Next.js, OpenAI Agents SDK, Dapr, Kafka
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server, Kubernetes cluster
**Project Type**: Full-stack web application with AI agent
**Performance Goals**: 1000+ concurrent users, <3s response time, 99% uptime
**Constraints**: <3s p95 response time, stateless backend services, secure JWT authentication
**Scale/Scope**: 1000+ concurrent users, 5-phase evolution, AI-native architecture

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development First: All implementation originates from validated specifications
- ✅ No Manual Coding: Code generated via Claude Code using Spec-Kit Plus
- ✅ Deterministic Agent Behavior: Following spec → plan → tasks → implement loop
- ✅ Traceability: Code traceable to speckit.specify (WHAT), speckit.plan (HOW), speckit.tasks (WORK UNIT)
- ✅ AI-Native Architecture: System designed for AI agents as first-class actors
- ✅ Monorepo Architecture: Frontend, backend, specs in single repository
- ✅ Stateless Services: Backend services remain stateless with state in databases/Dapr
- ✅ Cloud-Native by Design: Containerized and deployable to Kubernetes
- ✅ Technology Constraints: Python 3.13+, Next.js, FastAPI + SQLModel, PostgreSQL, etc.

## Project Structure

### Documentation (this feature)

```text
specs/1-todo-evolution/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py
│   │   ├── user.py
│   │   └── conversation.py
│   ├── services/
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   ├── auth_service.py
│   │   └── ai_integration_service.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── tasks.py
│   │   │   ├── users.py
│   │   │   └── auth.py
│   │   └── mcp/
│   │       └── tools.py
│   ├── mcp_server/
│   │   └── server.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── hooks/
├── app/
│   ├── api/
│   ├── tasks/
│   └── auth/
├── public/
└── package.json

agent/
├── src/
│   ├── agents/
│   │   └── todo_agent.py
│   ├── tools/
│   │   └── mcp_client.py
│   └── config/
│       └── agent_config.py
├── Dockerfile
└── requirements.txt

infra/
├── k8s/
│   ├── helm/
│   │   ├── backend/
│   │   ├── frontend/
│   │   └── agent/
│   ├── manifests/
│   └── dapr/
│       └── components/
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── agent.Dockerfile
└── kafka/
    └── topics/

specs/
├── 1-todo-evolution/
│   ├── spec.md
│   ├── plan.md
│   ├── research.md
│   ├── data-model.md
│   ├── quickstart.md
│   ├── contracts/
│   └── tasks.md
└── constitution.md

.history/
├── prompts/
│   └── todo-evolution/
└── adrs/

.env
Dockerfile
docker-compose.yml
README.md
pyproject.toml
next.config.js
```

**Structure Decision**: Multi-project structure selected to accommodate the complex requirements of a full-stack web application with AI agent and infrastructure components. The backend uses FastAPI with SQLModel for the API layer, the frontend uses Next.js for the web interface, and a separate agent module handles the AI integration via MCP tools.

## Phase-Wise Execution Plan

### Phase I – Foundation (Console App)
- Define task domain model with create, read, update, delete operations
- Implement console-based CRUD flow for task management
- Use in-memory state management for initial development
- Validate all functionality against specifications without persistence

### Phase II – Full-Stack Web System
- Define REST API contracts for task, user, and authentication endpoints
- Implement JWT-based authentication and user isolation
- Design database schema with PostgreSQL and SQLModel
- Create Next.js frontend with task management interface

### Phase III – AI Agent & MCP Integration
- Design MCP server exposing task operations as tools
- Implement AI agent using OpenAI Agents SDK
- Map natural language intents to specific task operations
- Store conversation state in database for continuity

### Phase IV – Local Kubernetes Deployment
- Create Dockerfiles for backend, frontend, and agent services
- Develop Helm charts for Kubernetes deployment
- Configure Minikube for local cloud-native deployment
- Set up Dapr sidecar configuration for infrastructure abstraction

### Phase V – Cloud-Native Event-Driven System
- Define Kafka topics for task lifecycle events
- Implement event schemas for reminders and recurring tasks
- Create async workflows for automated task management
- Add observability with logs, metrics, and tracing
- Set up CI/CD pipeline for automated deployments

## Architecture Blueprint

### High-Level System Diagram
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   End User      │    │   AI Agent       │    │  MCP Tools      │
│                 │    │                  │    │                 │
│  ┌───────────┐  │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│  │  Next.js  │  │    │ │OpenAI Agents │ │    │ │ Task CRUD   │ │
│  │ Frontend  │  │    │ │    SDK       │ │    │ │ Operations  │ │
│  └───────────┘  │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────┬───────┘    └─────────┬────────┘    └─────────┬───────┘
          │                      │                       │
          │                      │                       │
          │         ┌────────────▼──────────┐            │
          │         │     API Gateway       │◄───────────┘
          │         │    (FastAPI)          │
          │         └────────────┬──────────┘
          │                      │
          │         ┌────────────▼──────────┐
          │         │   Backend Services    │
          │         │                       │
          └────────►│  • Task Service       │
                    │  • Auth Service       │
                    │  • User Service       │
                    │  • AI Integration     │
                    └────────────┬──────────┘
                                 │
                    ┌────────────▼──────────┐
                    │     Data Layer        │
                    │                       │
                    │  • PostgreSQL         │
                    │  • Dapr State Store   │
                    │  • Kafka Topics       │
                    └───────────────────────┘
```

### Data Flow
1. User interacts with Next.js frontend (UI) or sends natural language to AI agent
2. Requests routed through API Gateway (FastAPI) with JWT authentication
3. Backend services process requests with proper user isolation
4. Data persisted in PostgreSQL with Dapr for state management
5. Events published to Kafka for async processing
6. MCP tools enable AI agent to perform task operations deterministically

### Phase Evolution
- **Phase I**: In-memory console → **Phase II**: Database persistence + web UI
- **Phase II**: Basic CRUD → **Phase III**: AI agent integration via MCP
- **Phase III**: Single instance → **Phase IV**: Kubernetes deployment
- **Phase IV**: Synchronous operations → **Phase V**: Event-driven architecture

## Key Decisions & Rationale

### 1. Monorepo vs Polyrepo Decision
- **Decision**: Monorepo approach selected
- **Rationale**: Enables easier coordination between frontend, backend, agent, and infrastructure components
- **Alternatives considered**: Separate repositories for each component
- **Trade-offs**: Simpler dependency management vs potential complexity in CI/CD

### 2. SQLModel + PostgreSQL Decision
- **Decision**: SQLModel with PostgreSQL as primary database
- **Rationale**: Aligns with constitution constraints and provides strong typing with SQL
- **Alternatives considered**: SQLAlchemy ORM, Django ORM, NoSQL options
- **Trade-offs**: Strong typing and validation vs potential complexity for simple operations

### 3. MCP Tool Boundaries Decision
- **Decision**: MCP tools restricted to task operations only
- **Rationale**: Maintains clear separation between AI agent and core business logic
- **Alternatives considered**: Direct AI agent database access, broader MCP scope
- **Trade-offs**: Better security and traceability vs potential performance overhead

### 4. Stateless Backend Enforcement Strategy
- **Decision**: All state stored in PostgreSQL/Dapr state stores
- **Rationale**: Enables horizontal scaling and fault tolerance as required by constitution
- **Alternatives considered**: In-memory caches, session storage
- **Trade-offs**: Scalability and resilience vs slight performance overhead

### 5. Kafka Usage vs Direct Async Processing
- **Decision**: Kafka for event-driven architecture in Phase V
- **Rationale**: Provides reliable messaging, replay capability, and decoupling
- **Alternatives considered**: Direct database polling, RabbitMQ, AWS SQS
- **Trade-offs**: Robust event handling vs operational complexity

### 6. Dapr Abstraction vs Native SDK Decision
- **Decision**: Dapr for infrastructure abstraction
- **Rationale**: Provides portability and consistent patterns across cloud providers
- **Alternatives considered**: Native Kubernetes APIs, cloud-specific services
- **Trade-offs**: Portability and consistency vs vendor-specific optimizations

### 7. Kubernetes Local-First Approach (Minikube)
- **Decision**: Minikube for local development mirroring production
- **Rationale**: Ensures local environment matches production architecture
- **Alternatives considered**: Docker Compose, direct local installation
- **Trade-offs**: Production parity vs local development convenience

## Agent Execution Model

### Planner Agent
- Responsibilities: Plan generation, architecture decisions, phase coordination
- Allowed actions: Create plan documents, define architecture, set phase boundaries
- Interaction: Works with spec → plan → tasks workflow

### Coder Agent
- Responsibilities: Code generation based on plans and tasks
- Allowed actions: Generate code from specifications, create contracts, implement services
- Guardrails: Cannot deviate from specs, must reference task IDs

### Reviewer Agent
- Responsibilities: Validate code against specifications and plans
- Allowed actions: Review generated code, check compliance with constitution
- Guardrails: Reject code that doesn't meet constitutional requirements

### Infrastructure Agent
- Responsibilities: Manage deployment configurations, containerization, K8s manifests
- Allowed actions: Generate Dockerfiles, Helm charts, K8s manifests
- Guardrails: Follow constitutional infrastructure patterns

## Validation & Quality Gates

### Phase Completion Checklist
- [ ] All functional requirements implemented and tested
- [ ] API contracts validated against specifications
- [ ] Security requirements met (JWT, user isolation)
- [ ] Performance targets achieved
- [ ] Documentation complete
- [ ] Tests passing (unit, integration, contract)

### Required Validations Before Moving Forward
- [ ] Spec compliance verified (every feature maps to spec)
- [ ] Constitution compliance confirmed
- [ ] All tests passing (no skipped tests)
- [ ] Code reviewed and approved
- [ ] Performance benchmarks met

### Reproducibility Verification
- [ ] Build succeeds from clean environment
- [ ] Deployment works in fresh Kubernetes cluster
- [ ] All dependencies properly specified
- [ ] Environment setup documented

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multi-repository structure | Need to separate frontend, backend, and agent concerns while maintaining monorepo benefits | Single codebase would mix concerns and make maintenance difficult |
| MCP server abstraction | Required for AI agent to interact with system while maintaining security boundaries | Direct database access would violate security and traceability requirements |
| Dapr integration | Needed for infrastructure abstraction and portability across cloud platforms | Native Kubernetes APIs would lock us into specific platform |
| Kafka for events | Required for reliable event processing and replay capability | Direct async processing would lack durability and ordering guarantees |