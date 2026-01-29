<!--
SYNC IMPACT REPORT
==================
Version change: 2.0.0 → 2.1.0

Major corrections:
- Removed custom user/password system (Better Auth is source of truth)
- Removed Phase V features (priority, due_date, events)
- Removed heavy tooling mandates not required by hackathon
- Fixed JWT model to Better Auth → FastAPI bridge
- Aligned strictly with official hackathon Phase II scope

Added:
- Explicit Phase III (MCP) forward compatibility
- Stateless backend enforcement
- Better Auth boundary rules
-->

# Todo Application Constitution  
## Phase II — Full-Stack Spec-Driven Web Application

---

## I. Spec-Driven Development First (NON-NEGOTIABLE)

All development MUST follow:

**Constitution → Specify → Plan → Tasks → Implement**

- No manual coding is allowed.
- All code MUST originate from approved specifications.
- All implementations MUST trace back to tasks.
- Specifications are the single source of truth.

Rationale: Prevents ad-hoc development, ensures traceability, enables Claude CLI automation, and prepares the system for Phase III–V.

---

## II. Full-Stack Quality Standard

### Backend (Python / FastAPI)

- Python 3.13+
- FastAPI best practices
- SQLModel ORM only (no raw SQL)
- Pydantic v2 models
- Type hints REQUIRED
- OpenAPI must be accurate
- Environment variables for all secrets
- Stateless architecture

### Frontend (Next.js / TypeScript)

- Next.js 16+ App Router
- TypeScript strict mode
- Server Components by default
- Client Components only when required
- Centralized API client
- No business logic in UI components
- ❌ No localStorage persistence for tasks

Rationale: Maintains correctness, testability, and AI-readiness.

---

## III. Testing Discipline (MANDATORY)

Backend must use `pytest`.

Tests MUST validate:

- Authentication success/failure
- JWT verification
- User data isolation
- Database persistence
- Error paths

Every major feature requires:

- Positive tests
- Negative tests
- Ownership tests

Rationale: Prevents data leaks, regressions, and hidden failures.

---

## IV. PostgreSQL Persistence Standard

- Neon Serverless PostgreSQL is REQUIRED
- SQLModel is REQUIRED
- Alembic migrations REQUIRED
- Tasks MUST persist in database
- Browser storage MUST NOT be used

Task table MUST include:

- id
- user_id (string from JWT)
- title
- description
- completed
- created_at
- updated_at

Rationale: Phase II transforms the system into a real multi-user platform.

---

## V. API & Frontend Contract Standard

### Backend

- Pure REST API
- Stateless
- JWT required on all protected routes
- Ownership enforced in every query
- Structured JSON errors

### Frontend

- Authentication handled ONLY by Better Auth
- JWT attached to every backend request
- Backend never manages sessions

Rationale: Clean separation of concerns and Phase III compatibility.

---

## VI. Measurable Acceptance Criteria

Every feature specification MUST include:

- Happy path
- Invalid input case
- Unauthorized case
- Cross-user protection case

All acceptance criteria MUST be testable.

Rationale: Enables automated verification and correct Claude task execution.

---

## VII. Monorepo Structure Mandate

Repository MUST contain:
/frontend (Next.js)
/backend (FastAPI)
/specs
CLAUDE.md
AGENTS.md or speckit.constitution


Frontend and backend MUST live in the same repository.

Rationale: Enables cross-stack reasoning and agent execution.

---

## VIII. JWT Authentication & User Isolation (NON-NEGOTIABLE)

### Auth Authority

- Better Auth is the ONLY authentication system.
- Backend never stores passwords.
- Backend never creates users.

### JWT Bridge Model

- Better Auth issues JWT
- Frontend attaches JWT
- FastAPI verifies JWT
- user_id extracted from token
- user_id enforced at query level

### Enforcement

- Every task row MUST contain user_id
- Every query MUST filter by user_id
- 401 if token invalid
- 403 if resource not owned

Rationale: Guarantees privacy, enables stateless scaling, protects MCP tools.

---

## IX. Security & Error Handling (NON-NEGOTIABLE)

Security:

- No secrets in code
- All inputs validated
- CORS explicitly configured
- ORM only
- HTTPS assumed in production

Errors:

- Structured JSON errors
- No stack traces in production
- User-friendly messages
- Server-side logging only

Rationale: Prevents leakage, protects users, supports safe scaling.

---

## X. Phase III Forward Compatibility

Phase II MUST produce a system that:

- is fully API-driven
- is stateless
- isolates users
- exposes task operations cleanly

All task logic MUST be callable as services.

Rationale: Prevents architectural rewrite in Phase III.

---

# Technical Constraints

## Locked Stack

Frontend:
- Next.js 16+
- TypeScript
- Better Auth

Backend:
- FastAPI
- SQLModel
- Neon PostgreSQL
- JWT verification library (jose / PyJWT)

Tooling:
- Spec-Kit Plus
- Claude CLI Agent

---

## Canonical Data Model

```python
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```
No advanced features in Phase II.

Canonical API Contract

Protected endpoints:

GET /api/tasks

POST /api/tasks

GET /api/tasks/{id}

PUT /api/tasks/{id}

DELETE /api/tasks/{id}

PATCH /api/tasks/{id}/complete


All requests require:
Authorization: Bearer <jwt>

Governance

* Constitution overrides all specs
* All changes require a Sync Impact Report
* Semantic versioning applies


Version: 2.1.0
Phase: Hackathon II — Phase II
Status: Ratified


---

If you want next, I can generate:

- ✅ Phase II `spec.md`
- ✅ Phase II `plan.md`
- ✅ Phase II `tasks.md`
- ✅ Claude CLI execution flow
- ✅ Neon + JWT implementation spec

Just tell me which one you want.
