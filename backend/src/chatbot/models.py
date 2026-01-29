"""Chatbot models for Phase III AI Chatbot.

Contains:
- Conversation: Chat session per user
- Message: Individual messages within conversations

Constitution Principle IV: SQLModel ORM only, no raw SQL queries.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Any, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import Index


# ============================================================================
# Message Role Enum
# ============================================================================

class MessageRole(str, Enum):
    """Message role enum per data-model.md."""
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


# ============================================================================
# Conversation Model
# ============================================================================

class Conversation(SQLModel, table=True):
    """
    Conversation model for chat history persistence.

    Fields per data-model.md:
    - id (int, primary key, auto-increment)
    - user_id (str from JWT, indexed, no FK constraint)
    - title (str, auto-generated from first message)
    - created_at (datetime UTC, auto-generated)

    Ownership enforcement:
    - user_id indexed for fast per-user queries
    - No foreign key constraint (Better Auth is external)
    - Application-level filtering required for queries
    """
    __tablename__ = "conversation"
    __table_args__ = (
        Index("ix_conversation_user_id", "user_id"),
        Index("ix_conversation_user_id_created_at", "user_id", "created_at"),
    )

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique conversation identifier (auto-increment)"
    )

    user_id: str = Field(
        nullable=False,
        description="User identifier from Better Auth JWT (no FK constraint)"
    )

    title: str = Field(
        default="New Conversation",
        max_length=255,
        nullable=False,
        description="Conversation title (auto-generated from first message)"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Conversation creation timestamp (UTC)"
    )

    # Relationship to messages (bidirectional)
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"}
    )


# ============================================================================
# Message Model
# ============================================================================

class Message(SQLModel, table=True):
    """
    Message model for storing chat messages.

    Fields per data-model.md:
    - id (int, primary key, auto-increment)
    - conversation_id (int, FK to Conversation.id)
    - role (enum: user/assistant/tool)
    - content (text, the message content)
    - metadata (JSON, optional tool call info)
    - created_at (datetime UTC, auto-generated)
    """
    __tablename__ = "message"
    __table_args__ = (
        Index("ix_message_conversation_id", "conversation_id"),
        Index("ix_message_conversation_id_created_at", "conversation_id", "created_at"),
    )

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique message identifier (auto-increment)"
    )

    conversation_id: int = Field(
        foreign_key="conversation.id",
        nullable=False,
        description="ID of the parent conversation"
    )

    role: MessageRole = Field(
        nullable=False,
        description="Message role: user, assistant, or tool"
    )

    content: str = Field(
        nullable=False,
        description="Message content text"
    )

    # Note: renamed from "metadata" which is reserved by SQLAlchemy
    extra_data: Optional[dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON),
        description="Optional extra data (tool_call_id, task_id, etc.)"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Message creation timestamp (UTC)"
    )

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


# ============================================================================
# Pydantic Schemas (Request/Response)
# ============================================================================

class ConversationCreate(SQLModel):
    """Conversation creation schema (title optional, user_id from JWT)."""
    title: Optional[str] = Field(default=None, max_length=255)


class ConversationResponse(SQLModel):
    """Conversation response schema with all fields."""
    id: int
    user_id: str
    title: str
    created_at: datetime
    message_count: int = 0


class ConversationListResponse(SQLModel):
    """Response model for listing conversations."""
    conversations: List["ConversationResponse"]
    total: int


class MessageCreate(SQLModel):
    """Message creation schema (role and content required)."""
    role: MessageRole = Field(default=MessageRole.USER)
    content: str = Field(min_length=1, max_length=10000)
    extra_data: Optional[dict[str, Any]] = None


class MessageResponse(SQLModel):
    """Message response schema with all fields."""
    id: int
    conversation_id: int
    role: MessageRole
    content: str
    extra_data: Optional[dict[str, Any]] = None
    created_at: datetime


class ChatMessageRequest(SQLModel):
    """Request schema for sending a chat message (user input only)."""
    content: str = Field(min_length=1, max_length=10000, description="User message content")


class ChatResponse(SQLModel):
    """Response schema for chat endpoint."""
    response: str = Field(description="Assistant response message")
    conversation_id: int = Field(description="Conversation ID")
    messages: List["MessageResponse"] = Field(default=[], description="All messages in conversation")


# Rebuild models to resolve forward references
ConversationListResponse.model_rebuild()
ChatResponse.model_rebuild()


__all__ = [
    "Conversation",
    "ConversationCreate",
    "ConversationResponse",
    "ConversationListResponse",
    "Message",
    "MessageRole",
    "MessageCreate",
    "MessageResponse",
    "ChatMessageRequest",
    "ChatResponse",
]
