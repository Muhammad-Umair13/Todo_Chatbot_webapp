"""SQLModel models for Phase II Todo Application.

Constitution Principle IV: SQLModel ORM only, no raw SQL queries.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import field_validator, computed_field


class Priority(str, Enum):
    """Task priority levels (reserved for future use)."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(SQLModel):
    """Base class containing common validation rules."""


class Task(TaskBase, table=True):
    """
    Canonical Task model for Phase II Todo Application.

    Fields strictly match Constitution Principle IV canonical data model:
    - id (int, primary key, auto-increment)
    - user_id (str from JWT, no FK constraint)
    - title (str, required, min 1 char)
    - description (str, optional, max 1000 chars)
    - completed (bool, default False)
    - created_at (datetime UTC, auto-generated)
    - updated_at (datetime UTC, auto-generated + auto-updated)

    Ownership enforcement:
    - user_id indexed for fast per-user queries
    - No foreign key constraint (Better Auth is external)
    - Application-level filtering required for queries
    """

    # Primary Key (auto-increment)
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier (auto-increment)"
    )

    # Ownership (from JWT, no FK constraint)
    user_id: str = Field(
        index=True,
        description="User identifier from Better Auth JWT (no FK constraint)"
    )

    # Task Data
    title: str = Field(
        min_length=1,
        max_length=200,
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
        default_factory=lambda: datetime.now(timezone.utc),
        description="Task creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update timestamp (UTC, auto-updated)"
    )


# SQLAlchemy event listener for auto-updating updated_at
from sqlalchemy import event
from sqlalchemy.orm import Mapper


@event.listens_for(Task, 'before_update')
def update_timestamp(mapper: Mapper, connection, target: Task) -> None:
    """
    Automatically update updated_at timestamp before any update.

    This implements plan.md requirement for auto-updating updated_at
    without requiring manual update calls in business logic.
    """
    target.updated_at = datetime.now(timezone.utc)


class TaskCreate(TaskBase):
    """Task creation model without id, timestamps, or user_id (will be set by system)."""

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)


class TaskUpdate(SQLModel):
    """Task update model with optional fields."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None


class TaskResponse(SQLModel):
    """Task response model with all fields including id and timestamps."""

    id: int
    user_id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskListResponse(SQLModel):
    """Response model for listing tasks."""

    tasks: list['TaskResponse']
    total: int


# Import Task model for Alembic env.py
__all__ = ["Task", "TaskCreate", "TaskUpdate", "TaskResponse", "TaskListResponse", "Priority"]
