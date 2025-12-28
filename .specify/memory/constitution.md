<!--
Sync Impact Report:
- Version change: 1.0.0 → 2.0.0
- Modified principles: All principles replaced with new ones
- Added sections: Tech Stack, Architecture, Security, File Structure, Dev Rules
- Removed sections: Old principles and constraints from Phase I
- Templates requiring updates: ✅ plan-template.md, ✅ spec-template.md, ✅ tasks-template.md
- Follow-up TODOs: None
-->
# Phase II Full-Stack Todo App Constitution

## Core Principles

### I. Tech Stack Compliance
The application MUST adhere to the specified technology stack: Next.js 16+ with App Router for frontend, FastAPI with SQLModel for backend, and Neon PostgreSQL for database. The application MUST use Better Auth with JWT for authentication and deploy to Vercel. The application MUST NOT introduce technologies outside of this approved stack without explicit architectural approval.

### II. Decoupled Architecture
The frontend and backend MUST be completely decoupled with a RESTful API using the /api prefix for all endpoints. The application MUST ensure proper separation of concerns between client and server components. The application MUST NOT have tight coupling between frontend and backend implementations.

### III. TypeScript Strict Mode
All frontend code MUST use TypeScript in strict mode with comprehensive type definitions. The application MUST NOT allow any code with implicit 'any' types or disabled strict checks. All API contracts MUST be strongly typed using shared interfaces or schemas to ensure type safety across the frontend-backend boundary.

### IV. Type Hints Mandatory (Backend)
Every Python function, method, and variable declaration in the backend MUST include appropriate type hints using modern Python type annotations. This ensures code clarity, enables better IDE support, and prevents type-related errors during development. The application MUST NOT be deployed without comprehensive type hint coverage.

### V. Comprehensive Error Handling
All operations in both frontend and backend MUST implement comprehensive error handling with appropriate logging and user feedback. The application MUST NOT expose internal error details to end users. Error boundaries MUST be implemented on the frontend and exception handlers on the backend to ensure graceful failure handling.

### VI. Input Validation
All user inputs MUST be validated on both frontend and backend before processing. Client-side validation provides immediate feedback while server-side validation ensures security. The application MUST NOT process unvalidated inputs under any circumstances. Validation MUST occur at the API layer to prevent malicious data from entering the system.

### VII. Security First
All security measures MUST be implemented according to the defined security requirements: password hashing with bcrypt, JWT secrets stored in environment variables, CORS configured to whitelist only the frontend domain, and no raw SQL queries. The application MUST NOT compromise on security measures for convenience. All authentication and authorization flows MUST be secure and follow industry best practices.

### VIII. Spec-Driven Development
All development MUST follow the established specifications using the Qwen CLI. Features SHOULD be implemented according to the documented requirements, and any deviations MUST be approved through the proper channels. Implementation MUST NOT proceed without clear specification. Each feature MUST have a corresponding git commit.

## Technology Stack

The application MUST use the following technology stack:
- Frontend: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- Backend: FastAPI, SQLModel, Python 3.13+
- Database: Neon PostgreSQL
- Authentication: Better Auth with JWT
- Deployment: Vercel

The application MUST NOT introduce technologies outside of this approved stack without explicit architectural approval.

## Architecture

The application MUST follow a decoupled frontend/backend architecture with a RESTful API. All API endpoints MUST be prefixed with /api. Authentication MUST use JWT tokens with a 7-day expiry. User data MUST be properly isolated so each user sees only their own tasks. The application MUST NOT allow cross-user data access.

## Security

The application MUST implement security measures including: password hashing with bcrypt, JWT secrets stored in environment variables, CORS configured to whitelist only the frontend domain, and no raw SQL queries. The application MUST NOT expose sensitive information in client-side code or logs. All API endpoints that require authentication MUST validate JWT tokens properly.

## File Structure

The application MUST follow the specified directory structure:
```
hackathon-todo/
├── phase1/         # Phase I untouched
├── frontend/       # Next.js application
├── backend/        # FastAPI application
└── specs/phase2/   # Specifications for Phase II
```

The application MUST NOT deviate from this structure without explicit approval.

## Constraints

The application MUST follow spec-driven development methodology using Qwen CLI. Manual coding MUST be avoided in favor of specification-driven implementation. Each feature MUST have a corresponding git commit. The application MUST NOT bypass the specification process or implement features without proper specifications.

## Error Handling

All user inputs MUST be validated before processing on both frontend and backend. The application MUST provide friendly, human-readable error messages instead of technical exceptions. The application MUST NOT crash under any circumstances, but instead handle errors gracefully and return to a stable state.

## Governance

This constitution supersedes all other development practices for this project. All amendments to this constitution MUST be documented and approved by the project maintainers. All pull requests and code reviews MUST verify compliance with these principles. The development team SHOULD refer to this constitution when making architectural or implementation decisions.

**Version**: 2.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-12-28
