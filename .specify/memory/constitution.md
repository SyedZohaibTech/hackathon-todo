<!-- SYNC IMPACT REPORT:
Version change: N/A (initial version) → 1.0.0
Added sections: Core Principles (6), Architectural Standards, Technology Constraints, Agent Rules, Quality & Engineering Standards, Phase Compliance Requirements
Modified principles: N/A
Removed sections: N/A
Templates requiring updates: ✅ .specify/templates/plan-template.md, ✅ .specify/templates/spec-template.md, ✅ .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Hackathon II – Spec-Driven Evolution of Todo Constitution

## Core Principles

### Spec-Driven Development First
All implementation MUST originate from validated specifications. No agent or human may write code without an approved spec and task.

### No Manual Coding
All code must be generated via Claude Code using Spec-Kit Plus. Humans may only refine specifications, not implementation.

### Deterministic Agent Behavior
Agents must behave predictably, following the same spec → plan → tasks → implement loop on every run.

### Traceability
Every line of code must be traceable to: speckit.specify (WHAT), speckit.plan (HOW), speckit.tasks (WORK UNIT).

### AI-Native Architecture
The system must be designed for AI agents as first-class actors, not as add-ons.

### No Agent Deviation
Agents MUST NOT: Invent features, Infer missing requirements, Change architecture without updating speckit.plan, Generate code without Task IDs, Bypass Spec-Kit lifecycle. Agents MUST: Stop and request clarification if a spec is incomplete, Reference specs using @specs/... paths, Respect Constitution > Specify > Plan > Tasks hierarchy.

## Architectural Standards

- Monorepo Architecture: Frontend, backend, specs, and agent instructions must live in a single repository.
- Stateless Services: Backend services must remain stateless. All state (tasks, conversations, messages) must persist in databases or Dapr state stores.
- Cloud-Native by Design: All services must be containerized and deployable to Kubernetes. Local deployment (Minikube) must mirror production architecture.
- Event-Driven Design (Phase V): Kafka (or Dapr Pub/Sub abstraction) must be used for: Task lifecycle events, Reminders, Recurring tasks, Audit logs.

## Technology Constraints

- Language: Python 3.13+
- Frontend: Next.js (App Router)
- Backend: FastAPI + SQLModel
- Database: Neon Serverless PostgreSQL
- AI: OpenAI Agents SDK
- Chat UI: OpenAI ChatKit
- MCP: Official Model Context Protocol SDK
- Deployment: Docker, Kubernetes, Helm
- Cloud-Native Runtime: Dapr
- Messaging: Kafka (or Kafka-compatible via Dapr)

No alternative stacks may be introduced without modifying this constitution.

## Agent Rules

- Agents MUST NOT:
  - Invent features
  - Infer missing requirements
  - Change architecture without updating speckit.plan
  - Generate code without Task IDs
  - Bypass Spec-Kit lifecycle

- Agents MUST:
  - Stop and request clarification if a spec is incomplete
  - Reference specs using @specs/... paths
  - Respect Constitution > Specify > Plan > Tasks hierarchy

## Quality & Engineering Standards

- Clean Architecture: Clear separation between UI, API, domain logic, and infrastructure.
- Reusable Intelligence: Agent Skills and Subagents must be reusable across phases where applicable.
- Security by Default: JWT-based authentication, User-level data isolation enforced on every operation, Secrets managed via environment variables or Dapr/Kubernetes secrets.
- Scalability: Architecture must support horizontal scaling without code changes.

## Phase Compliance Requirements

- Phase I: In-memory console app, spec-driven, no persistence.
- Phase II: Full-stack web app with authentication and persistent storage.
- Phase III: AI-powered chatbot using MCP tools for all task operations.
- Phase IV: Local Kubernetes deployment using Helm and Minikube.
- Phase V: Advanced cloud deployment with Kafka, Dapr, CI/CD, and monitoring.

Each phase must fully comply before proceeding to the next.

## Success Criteria

- 100% spec-driven implementation
- Zero manual code written
- All phases deployable and reproducible
- Stateless backend services
- AI agents correctly use MCP tools for task management
- Kubernetes deployments succeed locally and in cloud
- System behavior matches specifications exactly

## Failure Conditions

- Manual code written by humans
- Missing or undocumented specs
- Agent-generated code without Task references
- Architecture changes without spec updates
- State stored in memory instead of persistent layers

## Governance

This constitution governs all development activities. All implementation must comply with the principles and constraints outlined above. Any deviation requires a formal amendment to this constitution. Specifications must precede all implementation work, and all code must be traceable to approved specifications and tasks.

**Version**: 1.0.0 | **Ratified**: 2026-01-23 | **Last Amended**: 2026-01-23