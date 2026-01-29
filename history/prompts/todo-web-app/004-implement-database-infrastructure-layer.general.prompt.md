---
id: 004
title: implement-database-infrastructure-layer
stage: general
date: 2026-01-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-web-app
branch: main
user: user
command: Implement backend database infrastructure layer
labels: ["infrastructure","database","neon","fastapi","sqlmodel"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/core/config.py (updated)
 - backend/src/database.py (created/updated)
 - backend/src/main.py (updated)
 - backend/pyproject.toml (updated)
tests:
 - None (infrastructure-only phase)
---

## Prompt

TASK:
Implement the backend database infrastructure layer that binds Neon PostgreSQL to FastAPI.

SCOPE (infrastructure only — no business logic, no routes):

Create the following in backend/src:

1. database.py
   - Load DATABASE_URL from environment variables (.env supported)
   - Create SQLModel engine for Neon PostgreSQL
   - Enable pool_pre_ping
   - Provide a FastAPI dependency function get_session()
   - Ensure sessions are properly opened and closed
   - Must be fully type-annotated

2. core/config.py
   - Centralized environment loading
   - Read DATABASE_URL
   - Validate it exists, otherwise raise a clear startup error

3. main.py (update only if needed)
   - Initialize FastAPI app
   - Register startup/shutdown hooks if required
   - Ensure database layer can be imported without side effects

4. requirements/pyproject
   - Ensure dependencies include:
     fastapi, sqlmodel, psycopg[binary], python-dotenv, pydantic

NON-GOALS:
- Do NOT create models
- Do NOT create tables
- Do NOT create CRUD routes
- Do NOT create auth logic

QUALITY CONSTRAINTS:
- Follow Phase II Constitution
- SQLModel only (no raw SQL)
- No secrets in code
- Clear docstrings
- Fully testable design
- Stateless backend

OUTPUT REQUIREMENTS:
- Production-grade database layer
- Ready for Alembic integration
- Clean separation of concerns
- Passes mypy-style typing

After implementation, explain:
- How Neon is connected
- Where Alembic will hook in
- How other modules should import sessions

## Response snapshot

Successfully implemented the backend database infrastructure layer with the following changes:

**1. Updated core/config.py:**
- Made DATABASE_URL a required field (no default)
- Added field_validator to ensure DATABASE_URL exists and is properly formatted
- Validates that URL starts with "postgresql://" or "postgres://"
- Raises clear ValueError if missing or malformed

**2. Rewrote database.py:**
- Created SQLModel engine for Neon PostgreSQL with production-ready pooling:
  - pool_pre_ping=True (detects stale connections)
  - pool_size=10, max_overflow=20
  - pool_timeout=30, pool_recycle=3600
- Implemented get_session() as FastAPI dependency with Generator[Session, None, None] return type
- Sessions are context managers that auto-close
- Added get_engine() for Alembic access
- Added close_engine() for shutdown cleanup
- Fully type-annotated and documented

**3. Updated main.py:**
- Added close_engine() call in lifespan shutdown
- Logs database configuration (with credentials hidden)
- Database connections established lazily on first request
- Clean separation from business logic

**4. Updated pyproject.toml:**
- Added python-dotenv = "^1.0.0" dependency
- All required dependencies already present: fastapi, sqlmodel, psycopg2-binary, pydantic, pydantic-settings

## Outcome

- ✅ Impact: Foundation database layer implemented with Neon PostgreSQL connectivity
- 🧪 Tests: None (infrastructure-only, no business logic to test)
- 📁 Files: 4 files updated/created (config.py, database.py, main.py, pyproject.toml)
- 🔁 Next prompts: Database models, Alembic migrations, CRUD routes
- 🧠 Reflection: Implementation follows infrastructure layer pattern, ready for model and migration development

## Evaluation notes (flywheel)

- Failure modes observed: None - implementation successful
- Graders run and results (PASS/FAIL): Not applicable (infrastructure only)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add database models and Alembic migrations
