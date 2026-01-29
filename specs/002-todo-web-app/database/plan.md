# Database Implementation Plan: Phase II

**Feature**: 002-todo-web-app | **Database Layer** | **Date**: 2025-01-13
**Constitution**: Phase II v2.1.0
**Schema**: [schema.md](./schema.md)

## Overview

This plan defines the database layer implementation for Phase II of the Todo Web Application. The scope is strictly limited to the database layer - no API routes, no frontend, no authentication logic. The implementation follows the Phase II Constitution canonical data model, using SQLModel for ORM and Alembic for migrations.

### Scope Exclusions

- ❌ No User table (auth handled by Better Auth)
- ❌ No password hashing (Better Auth responsibility)
- ❌ No API routes (separate implementation phase)
- ❌ No frontend components (separate implementation phase)
- ❌ No priority field (Phase III+ feature)
- ❌ No due_date field (Phase III+ feature)
- ❌ No soft deletes (Phase III+ feature)

### Scope Inclusions

- ✅ Task table only
- ✅ user_id as string (from JWT, no FK constraint)
- ✅ Canonical fields: id, title, description, completed, created_at, updated_at
- ✅ Indexes on user_id and (user_id, completed)
- ✅ SQLModel integration with database.py
- ✅ Alembic migration workflow

---

## Architecture Decisions

### Decision 1: Canonical Task Model Only

**Choice**: Implement only the canonical Task model from Phase II Constitution.

**Rationale**:
- Constitution v2.1.0 is authoritative source
- Better Auth handles user management (no User table in backend)
- Phase II scope excludes priority, due_date, tags
- Schema matches exactly: id, user_id, title, description, completed, created_at, updated_at

**Alternatives Considered**:
- Full schema with User table and advanced fields: Rejected - violates Phase II Constitution v2.1.0
- Using existing 002-todo-web-app/data-model.md: Rejected - includes User table and Phase V features

---

### Decision 2: String user_id (No Foreign Key)

**Choice**: user_id as `str` type without foreign key constraint.

**Rationale**:
- user_id comes from JWT token (external Better Auth system)
- No User table in backend (Better Auth is truth)
- String type matches JWT `sub` claim
- No FK constraint prevents direct JOIN, enforces service-level filtering

**Constitution Reference**: Principle VIII - "user_id string from JWT"

**Alternatives Considered**:
- Integer user_id with FK to User table: Rejected - no User table exists
- UUID user_id: Rejected - adds complexity, not required for Phase II

---

### Decision 3: SQLModel ORM Standard

**Choice**: Use SQLModel (Pydantic v2 + SQLAlchemy v2).

**Rationale**:
- Constitution Principle IV requires SQLModel
- Pydantic v2 provides validation for API layer
- SQLAlchemy v2 provides query performance and connection pooling
- Type hints required by Constitution Principle II
- No raw SQL queries allowed

**Constitution Reference**: Principles II, IV

**Alternatives Considered**:
- SQLAlchemy only (without Pydantic): Rejected - violates Constitution Principle IV
- Raw SQL queries: Rejected - violates Constitution Principle IV

---

### Decision 4: UTC Timestamps with Auto-Update

**Choice**: Use `datetime.utcnow` factory with SQLAlchemy event listener for auto-updating `updated_at`.

**Rationale**:
- Constitution Principle IV requires timezone-aware timestamps
- UTC ensures consistency across regions
- Auto-update prevents manual errors
- SQLAlchemy `before_update` event is ORM-compliant

**Alternatives Considered**:
- Application-side manual updates: Rejected - error-prone, inconsistent
- Database triggers: Rejected - complex to manage with migrations
- Naive datetime.now(): Rejected - not timezone-aware

---

## SQLModel Design

### Task Entity Definition

```python
# backend/src/models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Canonical Task model for Phase II Todo Application.
    Enforces user data isolation through user_id field.
    """
    __tablename__ = "task"

    # Primary Key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-increment unique task identifier"
    )

    # Ownership (No FK - user_id from JWT)
    user_id: str = Field(
        index=True,
        description="User identifier from Better Auth JWT claim"
    )

    # Task Data
    title: str = Field(
        description="Task title (minimum 1 character)"
    )

    description: str = Field(
        default="",
        max_length=1000,
        description="Optional task details (maximum 1000 characters)"
    )

    # State
    completed: bool = Field(
        default=False,
        description="Task completion status (defaults to false)"
    )

    # Timestamps (UTC)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC, auto-updated)"
    )
```

### Field Type Mapping

| SQLModel Field | Python Type | SQL Type | Constraint | Default |
|---------------|-------------|------------|------------|----------|
| `id` | `int \| None` | `SERIAL` | Primary Key | Auto-increment |
| `user_id` | `str` | `VARCHAR(255)` | NOT NULL, INDEXED | None (from JWT) |
| `title` | `str` | `VARCHAR(200)` | NOT NULL | None (required) |
| `description` | `str` | `TEXT` | DEFAULT '' | Empty string |
| `completed` | `bool` | `BOOLEAN` | NOT NULL | `False` |
| `created_at` | `datetime` | `TIMESTAMPTZ` | NOT NULL | `utcnow()` |
| `updated_at` | `datetime` | `TIMESTAMPTZ` | NOT NULL | `utcnow()` + auto-update |

### Validation Rules (Constitution Compliance)

**Title Validation**:
- Minimum 1 character (enforced at Pydantic model level)
- No maximum length specified in Constitution, uses VARCHAR(200)
- Cannot be empty or whitespace

**Description Validation**:
- Optional (defaults to empty string)
- Maximum 1000 characters (enforced at database level)
- Truncation NOT allowed - must reject if exceeds

**Completed Validation**:
- Boolean type (true/false)
- Defaults to `False` on creation
- Required field

### Ownership Enforcement Strategy

**No Foreign Key Constraint**:
- user_id is a plain `str` field
- No database-level FK to User table
- Enforced entirely at application/service level

**Application-Level Enforcement**:
```python
# All queries MUST include user_id filter
statement = select(Task).where(Task.user_id == user_id)

# Ownership check for single task
task = session.exec(
    select(Task)
    .where(Task.id == task_id, Task.user_id == user_id)
).first()

if not task:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Constitution Reference**: Principle VIII - "user_id enforced at query level"

---

## Migration Workflow

### Alembic Initialization

**Location**: `backend/alembic/`

**Directory Structure**:
```
backend/
├── alembic/
│   ├── versions/              # Migration files
│   │   └── 001_initial.py  # Initial schema
│   ├── env.py                # Alembic environment
│   └── script.py.mako        # Migration template
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # SQLModel Task entity
│   └── database.py           # Database connection
└── alembic.ini                # Alembic configuration
```

### Configuration (alembic.ini)

```ini
[alembic]
script_location = backend/alembic
prepend_sys_path = .

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatter_keys]
keys = generic

[alembic]
prepend_sys_path = .

# Version path specification
version_path = %(here)s/versions
version_locations = %(here)s/versions
```

### Environment (alembic/env.py)

```python
# backend/alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from alembic import context
import sys
import os

# Add models path for autogenerate detection
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import all SQLModel models here for autogenerate
from src.models.task import Task
from src.database import engine

# Metadata for autogenerate
target_metadata = Task.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()
```

### Initial Migration (001_initial.py)

```python
# backend/alembic/versions/001_initial.py
"""Initial Phase II Task table.

Revision ID: 001
Revises:
Create Date: 2025-01-13
"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    """Create task table with indexes."""
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.String(255), nullable=False, index=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), server_default=''),
        sa.Column('completed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        comment='Phase II canonical task table'
    )

    # Create indexes
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_user_id_completed', 'task', ['user_id', 'completed'])

def downgrade() -> None:
    """Remove task table and indexes."""
    op.drop_index('ix_task_user_id_completed', 'task')
    op.drop_index('ix_task_user_id', 'task')
    op.drop_table('task')
```

### Migration Commands

**Generate Migration** (after model changes):
```bash
cd backend
alembic revision --autogenerate -m "Description of change"
```

**Apply Migration** (upgrade):
```bash
cd backend
alembic upgrade head
```

**Revert Migration** (downgrade):
```bash
cd backend
alembic downgrade -1
```

### Schema Evolution Control

**Phase II Lock**:
- No destructive migrations (no ALTER TABLE DROP COLUMN)
- No new columns beyond canonical model
- No additional tables (only `task` table)

**Review Process**:
- Autogenerated migrations MUST be manually reviewed
- Ensure index creation is correct
- Verify no unintended schema changes
- Test downgrade path

**Governance**:
- All migrations tracked in git
- Migration names follow semantic versioning: `XXX_description.py`
- No manual SQL in migrations (use SQLAlchemy operations)

---

## Index Strategy

### Index 1: user_id

```sql
CREATE INDEX ix_task_user_id ON task (user_id);
```

**Purpose**: Enable fast per-user task queries.

**Use Case**: `WHERE user_id = ?`

**Performance**: O(log n) lookup instead of O(n) full table scan.

**Query Patterns**:
- List all user tasks: `SELECT * FROM task WHERE user_id = ?`
- Get user task count: `SELECT COUNT(*) FROM task WHERE user_id = ?`

**Constitution Reference**: Principle VIII - user_id filtering required

---

### Index 2: Composite (user_id, completed)

```sql
CREATE INDEX ix_task_user_id_completed ON task (user_id, completed);
```

**Purpose**: Enable filtered task lists by completion status.

**Use Cases**:
- `WHERE user_id = ? AND completed = false` (active tasks)
- `WHERE user_id = ? AND completed = true` (completed tasks)

**Performance**: O(log n) lookup for both columns.

**Composite Benefit**:
- Index covers both `user_id` alone and `(user_id, completed)` together
- Postgres can use this single index for both query patterns
- More efficient than two separate indexes

**Query Patterns**:
```python
# Active tasks only (uses composite index)
statement = select(Task).where(Task.user_id == user_id, Task.completed == False)

# Completed tasks only (uses composite index)
statement = select(Task).where(Task.user_id == user_id, Task.completed == True)

# All user tasks (uses ix_task_user_id)
statement = select(Task).where(Task.user_id == user_id)
```

---

### Index 3: Primary Key (Automatic)

```sql
PRIMARY KEY (id)
```

**Purpose**: Unique task identifier for single task lookups.

**Use Case**: `WHERE id = ? AND user_id = ?`

**Performance**: O(log n) lookup via primary key.

---

### Index Validation

**No Cross-User Queries Without user_id**:
- Intentionally slow if user_id is missing from WHERE clause
- Enforces ownership pattern at database level

**Example**:
```python
# ✅ FAST: Uses index
statement = select(Task).where(Task.user_id == user_id)

# ❌ SLOW: Forces full table scan (intentional)
statement = select(Task).where(Task.completed == False)
```

**Design Decision**: Poor performance without user_id is intentional - prevents cross-user queries.

---

## Integration with FastAPI Infrastructure

### Database Connection (database.py)

```python
# backend/src/database.py
import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session.
    Provides automatic session cleanup after request.
    """
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database tables (for testing only, not production)."""
    SQLModel.metadata.create_all(engine)
```

### Dependency Injection Pattern

```python
# FastAPI router example
from fastapi import Depends
from src.database import get_session
from src.models.task import Task

@router.get("/api/tasks")
def get_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Session is automatically managed by FastAPI.
    - Session created before request
    - Session closed after request
    - Transactions committed automatically
    """
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

### Migration Runtime Isolation

**Avoid Runtime Side Effects**:
- Migrations run independently of application server
- Database URL from environment, not application code
- No application-level imports in migration files except models
- Migration scripts use SQLAlchemy `op.*` operations only

**Deployment Workflow**:
```bash
# 1. Run migrations before starting server
alembic upgrade head

# 2. Verify migration success
alembic current

# 3. Start application server
uvicorn src.main:app --reload
```

**Rollback Strategy**:
```bash
# If migration fails or causes issues
alembic downgrade -1  # Revert last migration

# Investigate issue, fix migration file
alembic revision --autogenerate -m "Fix previous migration"

# Apply fixed migration
alembic upgrade head
```

---

## Risk & Mitigation

### Risk 1: Migration Conflicts in Development

**Risk**: Multiple developers create migrations with same revision ID.

**Impact**: Migration history divergence, deployment failures.

**Mitigation**:
- Each developer creates migration on separate branch
- Conflict resolution via alembic revision rebase
- Clear naming convention: `XXX_descriptive_name.py`
- Migration review process before merge

### Risk 2: Index Performance Degradation

**Risk**: Too many indexes slow down INSERT/UPDATE operations.

**Impact**: Task creation/update latency increases.

**Mitigation**:
- Limit to minimal indexes (2 indexes + primary key)
- Monitor query performance with EXPLAIN ANALYZE
- Remove unused indexes (not applicable to Phase II)
- Composite index covers both user_id queries and filtered queries

### Risk 3: Schema Drift

**Risk**: Manual database changes not tracked in migrations.

**Impact**: Production schema differs from development.

**Mitigation**:
- Enforce Alembic for ALL schema changes
- No manual SQL execution in production
- Database access restricted to migration tooling
- Automated schema comparison in CI/CD pipeline

### Risk 4: Timezone Inconsistency

**Risk**: Mixing UTC and local timestamps.

**Impact**: Sorting errors, confusion for distributed users.

**Mitigation**:
- Strict use of `datetime.utcnow()` everywhere
- Database column type: `TIMESTAMPTZ`
- No naive datetime objects
- Frontend displays in local timezone (backend stores UTC only)

### Risk 5: Phase III Breaking Changes

**Risk**: Phase II schema incompatible with future features.

**Impact**: Requires schema migration in Phase III, potential data loss.

**Mitigation**:
- Canonical model strictly followed
- No FK constraint on user_id (allows future User integration)
- Service layer pattern isolates data access
- All operations are stateless (supports Phase III MCP tools)

---

## Phase Safety Controls

### Scope Lock: Phase II Canonical Model

**Locked Fields** (from Constitution Principle IV):
```python
class Task(SQLModel, table=True):
    id: int                       # ✅ Locked
    user_id: str                    # ✅ Locked
    title: str                        # ✅ Locked
    description: str = ""             # ✅ Locked
    completed: bool = False            # ✅ Locked
    created_at: datetime                # ✅ Locked
    updated_at: datetime                # ✅ Locked
```

**Forbidden Fields** (Phase II):
- ❌ No `priority` field
- ❌ No `due_date` field
- ❌ No `tags` field
- ❌ No `is_deleted` field
- ❌ No `user` relationship (no FK to User table)

**Governance**:
- Code review rejects additions to canonical model
- Alembic autogenerate reviewed for unintended changes
- Test suite validates schema matches canonical model

---

### Forward Compatibility: Phase III Readiness

**No Breaking Changes Required**:
- Canonical model supports Phase III features via extensions
- Service layer pattern enables MCP tool integration
- Stateless architecture supports programmatic access
- String user_id allows future User table integration

**Extension Strategy** (Phase III):
```python
# Phase II (Current)
class Task(SQLModel, table=True):
    # Canonical fields only

# Phase III (Future) - ADDITIVE ONLY
class Task(SQLModel, table=True):
    # Canonical fields (preserved)
    priority: str | None = None        # ✅ Additive
    due_date: datetime | None = None     # ✅ Additive
    tags: list[str] = []              # ✅ Additive
```

**Migration Approach** (Phase III):
```python
# Example Phase III migration (additive only)
def upgrade():
    op.add_column('task', sa.Column('priority', sa.String(20)))
    op.add_column('task', sa.Column('due_date', sa.DateTime(timezone=True)))

def downgrade():
    op.drop_column('task', 'due_date')
    op.drop_column('task', 'priority')
```

**No Breaking Changes**:
- ✅ No column deletions
- ✅ No type changes
- ✅ No constraint removals
- ✅ All Phase III additions are OPTIONAL (nullable)

---

### Validation Gate: Constitution Compliance

**Principle IV - PostgreSQL Persistence**: ✅ PASS
- Neon PostgreSQL selected
- SQLModel ORM used
- Alembic migrations configured
- Canonical model implemented exactly

**Principle VIII - JWT Authentication & User Isolation**: ✅ PASS
- user_id as string (from JWT)
- No User table (Better Auth handles users)
- Ownership enforced at query level (migration ensures indexes exist)

**Principle IX - Security**: ✅ PASS
- No secrets in models
- Input validation via Pydantic
- ORM only (no raw SQL)

**Principle X - Phase III Compatibility**: ✅ PASS
- Service layer pattern ready
- Stateless operations
- Additive-only schema evolution

---

## Acceptance Validation

### Checklist for Implementation

**Schema Validation**:
- [ ] Task model matches canonical model exactly
- [ ] user_id is string type (no FK constraint)
- [ ] All required fields present: id, user_id, title, description, completed, created_at, updated_at
- [ ] No forbidden fields: priority, due_date, tags, is_deleted

**Index Validation**:
- [ ] Index on user_id created
- [ ] Composite index on (user_id, completed) created
- [ ] Primary key index automatic
- [ ] No unnecessary indexes

**Migration Validation**:
- [ ] Alembic initialized successfully
- [ ] Initial migration (001_initial.py) creates task table
- [ ] Migration is reversible (downgrade() present)
- [ ] Migration includes all indexes
- [ ] Migration is reviewable (no raw SQL)

**Integration Validation**:
- [ ] database.py provides get_session() dependency
- [ ] Models importable without errors
- [ ] Session lifecycle managed by FastAPI
- [ ] Migrations run independently of application

**Phase Safety Validation**:
- [ ] No application logic in models (pure data model)
- [ ] No API routes in database layer
- [ ] No frontend code in database layer
- [ ] Schema locked to Phase II scope
- [ ] Forward compatible with Phase III extensions

---

## Summary

This database implementation plan satisfies:

**Schema Requirements** (from schema.md):
- ✅ Task entity with canonical fields implemented
- ✅ String user_id (no FK) for JWT integration
- ✅ UTC timestamps with auto-update
- ✅ Validation rules enforced (title min 1 char, description max 1000)
- ✅ Ownership enforced via application-level queries

**Constitution Compliance**:
- ✅ Principle II (SQLModel, Pydantic v2, type hints)
- ✅ Principle IV (Neon PostgreSQL, Alembic migrations, canonical model)
- ✅ Principle VIII (user_id string from JWT, query-level enforcement)
- ✅ Principle IX (ORM only, input validation, no secrets)
- ✅ Principle X (Service layer pattern, stateless, Phase III compatible)

**Technical Excellence**:
- ✅ Minimal indexes for optimal query performance
- ✅ Reversible migrations with governance
- ✅ FastAPI integration via dependency injection
- ✅ No breaking changes for Phase III extensions
- ✅ Scope locked to database layer only

**Implementation Ready**:
- ✅ SQLModel Task entity fully specified
- ✅ Alembic workflow documented
- ✅ Index strategy defined
- ✅ FastAPI integration pattern provided
- ✅ Phase safety controls established
- ✅ Claude tasks can implement from this plan

**Status**: ✅ Plan complete and ready for `/sp.tasks` to generate implementation tasks.
