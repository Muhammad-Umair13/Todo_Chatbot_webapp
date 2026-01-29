"""
Models package.

Phase II: Full-Stack Multi-User Web Todo Application
Phase III: AI Chatbot - Models in chatbot package
"""
from .base import SQLModel
from .user import User, UserCreate, UserLogin, UserResponse, TokenResponse, hash_password, verify_password
from .task import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    Priority,
)

# Phase III: Chat models are now in chatbot package
# Import from there: from ..chatbot.models import Conversation, Message, etc.

__all__ = [
    # Base
    "SQLModel",
    # User models
    "User",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "hash_password",
    "verify_password",
    # Task models
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    "Priority",
]
