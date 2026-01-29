# Data Model: Full-Stack Multi-User Web Todo Application

**Feature**: 002-todo-web-app
**Date**: 2026-01-05
**Purpose**: Database schema design and entity relationships

## Overview

This document defines the data model for the multi-user todo application. The schema enforces user data isolation, referential integrity, and supports all functional requirements defined in spec.md.

---

## Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
│─────────────────────│
│ id: SERIAL PK       │
│ email: VARCHAR(255) │◄───────┐
│   UNIQUE, NOT NULL  │        │
│ hashed_password     │        │
│   VARCHAR(255)      │        │
│ name: VARCHAR(255)  │        │
│ created_at: TIMESTAMPTZ      │
│ updated_at: TIMESTAMPTZ      │
└─────────────────────┘        │
                               │
                               │ One-to-Many
                               │ (user_id FK)
                               │
┌─────────────────────┐        │
│       Task          │        │
│─────────────────────│        │
│ id: SERIAL PK       │        │
│ user_id: INTEGER    │────────┘
│   FK → User(id)     │
│   NOT NULL, INDEX   │
│ title: VARCHAR(200) │
│   NOT NULL          │
│ description: TEXT   │
│   DEFAULT ''        │
│ completed: BOOLEAN  │
│   DEFAULT false     │
│ priority: VARCHAR(20)│
│   CHECK IN (...)    │
│ due_date: TIMESTAMPTZ│
│ created_at: TIMESTAMPTZ
│ updated_at: TIMESTAMPTZ
└─────────────────────┘
```

**Relationship**: One User has Many Tasks. Each Task belongs to exactly one User.

---

## Entity Definitions

### User Entity

**Purpose**: Represents a registered user account with authentication credentials.

**SQLModel Definition**:
```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    """User account with authentication credentials."""
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        nullable=False,
        description="User email address (used for login)"
    )
    hashed_password: str = Field(
        max_length=255,
        nullable=False,
        description="Bcrypt hashed password"
    )
    name: str = Field(
        max_length=255,
        nullable=False,
        description="User display name"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last account update timestamp"
    )

    # Relationships
    tasks: list["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

**Fields**:
- **id** (Primary Key): Auto-incrementing unique identifier
- **email** (Unique, Indexed): User email for login, must be unique across system
- **hashed_password**: Bcrypt hash (never store plaintext)
- **name**: User display name
- **created_at**: Account registration timestamp
- **updated_at**: Last modification timestamp

**Validation Rules**:
- Email must be valid format (validated by Pydantic schema)
- Password must be >= 8 characters (validated before hashing)
- Name cannot be empty

**Indexes**:
- `PRIMARY KEY (id)`
- `UNIQUE INDEX idx_users_email (email)`

**Constraints**:
- email UNIQUE NOT NULL
- hashed_password NOT NULL
- name NOT NULL

---

### Task Entity

**Purpose**: Represents a todo item owned by a specific user.

**SQLModel Definition**:
```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(SQLModel, table=True):
    """Task (todo item) owned by a user."""
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
        description="Owner user ID (enforces data isolation)"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False,
        description="Task title"
    )
    description: str = Field(
        default="",
        max_length=1000,
        nullable=False,
        description="Optional task description"
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        index=True,
        description="Completion status"
    )
    priority: Priority | None = Field(
        default=None,
        nullable=True,
        description="Task priority (low/medium/high)"
    )
    due_date: datetime | None = Field(
        default=None,
        nullable=True,
        index=True,
        description="Optional due date"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp"
    )

    # Relationships
    user: User = Relationship(back_populates="tasks")
```

**Fields**:
- **id** (Primary Key): Auto-incrementing unique identifier
- **user_id** (Foreign Key, Indexed): Reference to owning user, enforces data isolation
- **title** (Required): Task title (1-200 characters)
- **description** (Optional): Detailed description (max 1000 characters)
- **completed** (Boolean, Indexed): Completion status (default: false)
- **priority** (Enum): Optional priority level (low, medium, high)
- **due_date** (Optional, Indexed): Optional due date for the task
- **created_at**: Task creation timestamp
- **updated_at**: Last modification timestamp (automatically updated)

**Validation Rules**:
- Title must be 1-200 characters (non-empty, not too long)
- Description max 1000 characters
- Priority must be one of: low, medium, high (if provided)
- user_id must reference existing user

**Indexes**:
- `PRIMARY KEY (id)`
- `INDEX idx_tasks_user_id (user_id)` - Optimize user task queries
- `INDEX idx_tasks_completed (completed)` - Filter by completion status
- `INDEX idx_tasks_due_date (due_date)` - Sort/filter by due date

**Constraints**:
- user_id FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE
- title NOT NULL
- completed NOT NULL
- priority CHECK (priority IN ('low', 'medium', 'high') OR priority IS NULL)

**Cascade Behavior**:
- ON DELETE CASCADE: Deleting a user automatically deletes all their tasks

---

## Database Schema (SQL)

### users Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_users_email ON users(email);

COMMENT ON TABLE users IS 'User accounts with authentication credentials';
COMMENT ON COLUMN users.id IS 'Unique user identifier';
COMMENT ON COLUMN users.email IS 'User email address (login)';
COMMENT ON COLUMN users.hashed_password IS 'Bcrypt hashed password (never plaintext)';
COMMENT ON COLUMN users.name IS 'User display name';
```

### tasks Table

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    completed BOOLEAN NOT NULL DEFAULT false,
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high')),
    due_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_date ON tasks(due_date) WHERE due_date IS NOT NULL;

COMMENT ON TABLE tasks IS 'Todo items owned by users';
COMMENT ON COLUMN tasks.user_id IS 'Owner user ID (enforces data isolation)';
COMMENT ON COLUMN tasks.title IS 'Task title (required, 1-200 chars)';
COMMENT ON COLUMN tasks.completed IS 'Completion status';
COMMENT ON COLUMN tasks.priority IS 'Optional priority level';
COMMENT ON COLUMN tasks.due_date IS 'Optional due date';
```

---

## Data Isolation Strategy

### User Data Isolation Rules

**Constitutional Requirement** (Principle VIII):
> EVERY todo item MUST have a user_id foreign key. Database queries MUST filter by authenticated user_id. NO cross-user data access permitted.

**Enforcement Mechanisms**:

1. **Database Level**: Foreign key constraint ensures every task has a valid user_id
2. **ORM Level**: SQLModel relationships enforce owner references
3. **Service Level**: All queries filtered by authenticated user_id
4. **API Level**: Middleware extracts user_id from JWT, passes to services

**Query Pattern (REQUIRED)**:
```python
# ✅ CORRECT: Always filter by user_id
async def get_user_tasks(db: Session, user_id: int) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user_id).all()

# ❌ WRONG: No user_id filter allows cross-user access
async def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()  # VIOLATES PRINCIPLE VIII
```

**Ownership Validation** (Update/Delete):
```python
async def update_task(db: Session, task_id: int, user_id: int, data: TaskUpdate):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id  # Ownership check
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task...
```

---

## State Transitions

### Task Lifecycle

```
┌─────────────┐
│   Created   │  completed=false
└──────┬──────┘
       │
       │ (User marks complete)
       ▼
┌─────────────┐
│  Completed  │  completed=true
└──────┬──────┘
       │
       │ (User toggles back)
       ▼
┌─────────────┐
│   Active    │  completed=false
└──────┬──────┘
       │
       │ (User deletes)
       ▼
┌─────────────┐
│   Deleted   │  Removed from database
└─────────────┘
```

**Valid Transitions**:
- Created → Completed (mark complete)
- Completed → Active (toggle back)
- Any State → Deleted (permanent removal)

**Invalid Transitions**:
- Deleted → Any (no restoration in Phase II)

---

## Migration Strategy

### Alembic Migrations

**Initial Migration** (create tables):
```bash
alembic revision --autogenerate -m "Create users and tasks tables"
alembic upgrade head
```

**Migration File Structure**:
```
alembic/
├── versions/
│   └── 001_create_users_tasks.py
├── env.py
└── alembic.ini
```

**Sample Migration**:
```python
# alembic/versions/001_create_users_tasks.py
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_index('idx_users_email', 'users', ['email'])

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('description', sa.Text(), server_default='', nullable=False),
        sa.Column('completed', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('priority', sa.String(20)),
        sa.Column('due_date', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'])

def downgrade():
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## Query Optimization

### Index Strategy

**users Table**:
- `id` (PK): Auto-indexed, used for foreign key lookups
- `email` (UNIQUE): Indexed for login queries

**tasks Table**:
- `id` (PK): Auto-indexed
- `user_id`: **Critical** - All queries filter by this
- `completed`: Filter completed vs active tasks
- `due_date`: Sort/filter by due date (partial index WHERE due_date IS NOT NULL)

### Query Performance

**Expected Query Patterns**:
1. **List User Tasks**: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
   - Uses: idx_tasks_user_id
   - Expected: < 10ms for 1000 tasks

2. **Get Single Task**: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`
   - Uses: Primary key + idx_tasks_user_id
   - Expected: < 5ms

3. **Filter by Completion**: `SELECT * FROM tasks WHERE user_id = ? AND completed = ?`
   - Uses: idx_tasks_user_id + idx_tasks_completed
   - Expected: < 10ms

4. **Filter by Due Date**: `SELECT * FROM tasks WHERE user_id = ? AND due_date < ?`
   - Uses: idx_tasks_user_id + idx_tasks_due_date
   - Expected: < 10ms

---

## Summary

The data model implements:
- ✅ User authentication with hashed passwords
- ✅ User data isolation via user_id foreign keys
- ✅ Referential integrity with CASCADE deletes
- ✅ Optimized indexes for common query patterns
- ✅ Constitutional compliance (Principles IV, VIII)
- ✅ All specification requirements (37 functional requirements supported)

**Ready for**: API contract definition and implementation.
