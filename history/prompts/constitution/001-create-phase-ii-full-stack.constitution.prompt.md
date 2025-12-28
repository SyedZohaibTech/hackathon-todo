---
id: 001
title: Create Phase II Full-Stack Todo App Constitution
stage: constitution
date_iso: 2025-12-28
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "full-stack", "nextjs", "fastapi", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
prompt_text: |
  /sp.constitution Create Phase II Full-Stack Todo App constitution.

  **Include:**
  1. **Tech Stack (NON-NEGOTIABLE):**
     - Frontend: Next.js 16+ (App Router), TypeScript, Tailwind
     - Backend: FastAPI, SQLModel, Python 3.13+
     - Database: Neon PostgreSQL
     - Auth: Better Auth + JWT
     - Deploy: Vercel

  2. **Architecture:**
     - Decoupled frontend/backend
     - RESTful API (/api prefix)
     - JWT for auth (7-day expiry)
     - User data isolation (each user sees only their tasks)

  3. **Code Standards:**
     - TypeScript strict mode (frontend)
     - Type hints mandatory (backend)
     - Error handling on all operations
     - Input validation both sides

  4. **Security:**
     - Password hashing (bcrypt)
     - JWT secret in env vars
     - CORS whitelist frontend only
     - No raw SQL queries

  5. **File Structure:**
  ```
  hackathon-todo/
  ├── phase1/         # Phase I untouched
  ├── frontend/       # Next.js
  ├── backend/        # FastAPI
  └── specs/phase2/   # Specs
  ```

  6. **Dev Rules:**
     - Spec-driven with Qwen CLI
     - No manual coding
     - Git commit per feature
response_text: |
  Successfully updated the constitution for the Phase II Full-Stack Todo App with version 2.0.0. The new constitution includes:
  
  1. Core principles for the new tech stack (Next.js, FastAPI, Neon PostgreSQL)
  2. Architecture guidelines for decoupled frontend/backend
  3. Code standards for TypeScript strict mode and Python type hints
  4. Security requirements including bcrypt, JWT, CORS, and no raw SQL
  5. File structure specification
  6. Development rules for spec-driven development
  
  The constitution was updated with all the required elements from the user's request, and templates were checked for consistency.
outcome: |
  The constitution for the Phase II Full-Stack Todo App has been successfully created and updated at .specify/memory/constitution.md. The version was bumped from 1.0.0 to 2.0.0 to reflect the major changes in technology stack and principles. All required elements from the user's request were incorporated.
evaluation: |
  The constitution update was completed successfully with all required elements included. The document now properly reflects the technology stack, architecture, security requirements, and development practices for the Phase II Full-Stack Todo App. The templates were checked for consistency and no updates were needed.
---

# Create Phase II Full-Stack Todo App Constitution

This PHR documents the creation of the constitution for the Phase II Full-Stack Todo App with the specified technology stack and requirements.