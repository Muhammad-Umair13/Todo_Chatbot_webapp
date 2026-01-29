#!/usr/bin/env python3
"""Test file to isolate the import issue."""

from sqlmodel import SQLModel, Field
from datetime import datetime
import bcrypt
from pydantic import Field as PydanticField, EmailStr
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique user identifier (auto-increment)"
    )

    email: str = Field(
        unique=True,
        index=True,
        description="Unique email address"
    )

    name: str = Field(
        max_length=100,
        description="User display name"
    )

    hashed_password: str = Field(
        description="Bcrypt hashed password"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC)"
    )

print("User model defined successfully!")