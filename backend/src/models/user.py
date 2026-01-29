"""User model and authentication for Phase II Todo Application.

Constitution Principle III: JWT required on protected routes.
Better Auth is the external authentication authority.
This module provides local user storage for login/register flows.
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
import bcrypt
from pydantic import Field as PydanticField
from typing import Optional


class User(SQLModel, table=True):
    """
    User model for local authentication.

    This stores user credentials for the login/register flow.
    JWT tokens are issued based on this user data.

    Fields:
    - id: Primary key
    - email: Unique email address
    - name: User display name
    - hashed_password: Bcrypt hashed password
    - created_at: Account creation timestamp
    - updated_at: Last update timestamp
    """

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


class UserCreate(SQLModel):
    """User registration request model."""

    email: str = Field(..., description="User email address")
    name: str = Field(min_length=2, max_length=100, description="User display name")
    password: str = Field(min_length=8, description="Plain text password (will be hashed)")


class UserLogin(SQLModel):
    """User login request model."""

    email: str = Field(..., description="User email address")
    password: str = Field(description="Plain text password")


class UserResponse(SQLModel):
    """User response model (without password)."""

    id: int
    email: str
    name: str
    created_at: datetime


class TokenResponse(SQLModel):
    """JWT token response model."""

    access_token: str
    token_type: str = "Bearer"
    user: UserResponse


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


__all__ = [
    "User",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "hash_password",
    "verify_password",
]