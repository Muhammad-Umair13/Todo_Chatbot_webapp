---
id: "002"
title: "Create implementation plan for full-stack web app"
stage: "plan"
date: "2026-01-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-web-app"
branch: "002-todo-web-app"
user: "local user"
command: "/sp.plan"
labels: ["plan", "architecture", "monorepo", "fullstack", "phase-ii"]
links:
  spec: "specs/002-todo-web-app/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-todo-web-app/plan.md"
  - "specs/002-todo-web-app/research.md"
  - "specs/002-todo-web-app/data-model.md"
  - "specs/002-todo-web-app/quickstart.md"
  - "specs/002-todo-web-app/contracts/auth.yaml"
  - "specs/002-todo-web-app/contracts/tasks.yaml"
tests:
  - "none"
---

## Prompt

Create speckit.plan for Phase II based strictly on speckit.specify.

Include:
- High-level system architecture
- Frontend (Next.js) responsibilities
- Backend (FastAPI) responsibilities
- Authentication flow using Better Auth + JWT
- API request/response lifecycle
- Database schema overview
- Monorepo folder structure
- Environment variable strategy
- Deployment strategy (Vercel + API)

No implementation details yet.

## Response snapshot

Created comprehensive implementation plan with all Phase 0 and Phase 1 artifacts:

**plan.md** - Implementation Plan:
- Summary: Monorepo architecture with Next.js 16+ frontend, FastAPI backend, JWT auth, Neon PostgreSQL
- Technical Context: All fields filled (Python 3.13+, TypeScript 5+, complete dependency list)
- Constitution Check: All 9 principles validated ✅ PASS
- Project Structure: Detailed monorepo layout with apps/web, apps/api, packages/types
- Architecture Overview: Complete system diagrams and component responsibilities
- Authentication Flow: Registration, login, token refresh, logout flows documented
- API Lifecycle: Example request/response flow for task creation
- Database Schema: SQL DDL with indexes and constraints
- Environment Strategy: Frontend and backend .env templates
- Deployment Strategy: Vercel (frontend) + Railway/Render (backend) + Neon (database)

**research.md** - Technology Research (Phase 0):
- 10 major research topics with decisions documented
- Monorepo: Turborepo + pnpm workspaces selected
- Authentication: Custom JWT with python-jose, Better Auth patterns frontend
- Frontend: Next.js App Router with route groups
- Backend: FastAPI clean architecture (routers → services → models)
- ORM: SQLModel with Alembic migrations
- Database: Neon Serverless PostgreSQL with connection pooling
- State Management: React Context + Hooks (minimal per constitution)
- API Contracts: OpenAPI YAML + FastAPI auto-generation
- Testing: pytest + React Testing Library
- Error Handling: Structured JSON responses + logging strategy

**data-model.md** - Database Design (Phase 1):
- Entity Relationship Diagram (User ← Task)
- User entity: id, email (unique), hashed_password, name, timestamps
- Task entity: id, user_id (FK), title, description, completed, priority, due_date, timestamps
- SQLModel definitions with complete field specifications
- SQL DDL with indexes (user_id, completed, due_date)
- Data isolation strategy with query patterns
- State transitions diagram
- Alembic migration strategy
- Query optimization guide

**contracts/** - API Contracts (Phase 1):
- **auth.yaml**: Complete OpenAPI 3.0 spec for authentication
  - POST /auth/register - User registration
  - POST /auth/login - Email/password authentication
  - POST /auth/refresh - Token refresh with rotation
  - POST /auth/logout - Refresh token invalidation
  - Full request/response schemas with examples

- **tasks.yaml**: Complete OpenAPI 3.0 spec for task management
  - GET /tasks - List user tasks (with filters/sorting)
  - POST /tasks - Create task
  - GET /tasks/{id} - Get single task
  - PUT /tasks/{id} - Update task
  - DELETE /tasks/{id} - Delete task
  - PATCH /tasks/{id}/complete - Toggle completion
  - Full CRUD with ownership validation

**quickstart.md** - Local Development Guide (Phase 1):
- Prerequisites (Node 20+, Python 3.13+, PostgreSQL/Neon)
- Project setup (clone, install dependencies)
- Database setup (local PostgreSQL or Neon)
- Environment configuration (.env templates)
- Database migrations (Alembic commands)
- Running the application (Turborepo dev commands)
- Testing (pytest + React Testing Library)
- Code quality (linting, formatting, type checking)
- Development workflow (TDD cycle)
- Troubleshooting guide
- Useful commands reference

## Outcome

- ✅ Impact: Complete architectural design and planning artifacts ready for task generation
- 🧪 Tests: All constitutional principles validated and passed
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/auth.yaml, contracts/tasks.yaml
- 🔁 Next prompts: /sp.tasks to generate executable task list organized by user stories
- 🧠 Reflection: Planning phase complete with comprehensive documentation. All technology decisions researched and justified. Database schema designed with proper isolation. API contracts defined following OpenAPI 3.0 standard. Development environment documented for quick onboarding.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): Constitution Check - ALL PASS (9/9 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
