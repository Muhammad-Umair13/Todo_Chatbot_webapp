"""
Chatbot package for Phase III AI Todo Chatbot.

This package contains all chatbot-related components:
- models: Conversation and Message SQLModel models
- services: ChatService (CRUD) and AgentService (OpenAI + MCP tools)
- router: FastAPI endpoints for chat API
"""
from .models import (
    Conversation,
    ConversationCreate,
    ConversationResponse,
    ConversationListResponse,
    Message,
    MessageRole,
    MessageCreate,
    MessageResponse,
    ChatMessageRequest,
    ChatResponse,
)
from .services import ChatService, AgentService, MCPTools, get_agent_service
from .router import router as chat_router

__all__ = [
    # Models
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
    # Services
    "ChatService",
    "AgentService",
    "MCPTools",
    "get_agent_service",
    # Router
    "chat_router",
]
