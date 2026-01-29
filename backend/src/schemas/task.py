"""Pydantic schemas for Task API endpoints.

These schemas define the request/response models for the Task API.
They are used for validation and serialization in FastAPI endpoints.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str
    description: str = ""
    completed: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, bread, eggs, and fruit",
                "completed": False
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "description": "Updated description",
                "completed": True
            }
        }


class TaskResponse(BaseModel):
    """Schema for reading a task (includes all fields including id and timestamps)."""

    id: int
    user_id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user-123",
                "title": "Sample task",
                "description": "This is a sample task",
                "completed": False,
                "created_at": "2025-01-14T10:00:00Z",
                "updated_at": "2025-01-14T10:00:00Z"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for task list response."""

    tasks: List[TaskResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "user_id": "user-123",
                        "title": "Sample task",
                        "description": "This is a sample task",
                        "completed": False,
                        "created_at": "2025-01-14T10:00:00Z",
                        "updated_at": "2025-01-14T10:00:00Z"
                    }
                ],
                "total": 1
            }
        }