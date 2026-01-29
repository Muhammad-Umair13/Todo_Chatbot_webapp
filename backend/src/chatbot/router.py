"""Chat router for Phase III AI Chatbot.

Constitution Principle III: JWT required on protected routes.
All endpoints require authentication and enforce user ownership.

Endpoints:
- POST /api/chat/conversations - Create new conversation
- GET /api/chat/conversations - List user's conversations
- GET /api/chat/conversations/{id} - Get conversation details
- DELETE /api/chat/conversations/{id} - Delete conversation
- POST /api/chat/conversations/{id}/messages - Send chat message
- POST /api/chat/message - Quick chat (auto-creates conversation)
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from loguru import logger

from ..database import get_session
from ..auth.dependencies import AuthenticatedUser, get_current_user
from .services import ChatService, get_agent_service
from .models import (
    MessageRole,
    MessageResponse,
    ChatMessageRequest,
    ConversationCreate,
    ConversationResponse,
    ConversationListResponse,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["chat"],
    responses={
        401: {"description": "Unauthorized - Missing or invalid JWT"},
        404: {"description": "Conversation not found"},
    }
)


# ============================================================================
# Conversation Endpoints
# ============================================================================

@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new conversation",
)
async def create_conversation(
    conversation_data: ConversationCreate = None,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> ConversationResponse:
    """Create a new conversation for the authenticated user."""
    title = conversation_data.title if conversation_data else None
    conversation = ChatService.create_conversation(
        session=session,
        user_id=current_user.user_id,
        title=title
    )
    logger.info(f"Created conversation {conversation.id} for user {current_user.user_id}")
    return conversation


@router.get(
    "/conversations",
    response_model=ConversationListResponse,
    summary="List user's conversations",
)
async def list_conversations(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> ConversationListResponse:
    """Get all conversations for the authenticated user."""
    conversations = ChatService.list_conversations(
        session=session,
        user_id=current_user.user_id,
        limit=limit,
        offset=offset
    )
    return ConversationListResponse(conversations=conversations, total=len(conversations))


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get conversation details",
)
async def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> ConversationResponse:
    """Get a specific conversation by ID."""
    conversation = ChatService.get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.user_id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "conversation_not_found", "message": f"Conversation {conversation_id} not found"}
        )
    return conversation


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a conversation",
)
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> None:
    """Delete a conversation and all its messages."""
    deleted = ChatService.delete_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.user_id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "conversation_not_found", "message": f"Conversation {conversation_id} not found"}
        )
    logger.info(f"Deleted conversation {conversation_id}")


# ============================================================================
# Message Endpoints
# ============================================================================

@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=List[MessageResponse],
    summary="Get conversation messages",
)
async def get_messages(
    conversation_id: int,
    limit: int = 50,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> List[MessageResponse]:
    """Get all messages in a conversation."""
    conversation = ChatService.get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=current_user.user_id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "conversation_not_found", "message": f"Conversation {conversation_id} not found"}
        )

    return ChatService.load_history(session=session, conversation_id=conversation_id, limit=limit)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=dict,
    summary="Send a chat message",
    description="Send a message to the AI assistant and get a response.",
)
async def send_message(
    conversation_id: int,
    message: ChatMessageRequest,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> dict:
    """
    Send a chat message and get AI response.

    Data Flow:
    1. Verify JWT and extract user_id
    2. Load conversation from DB
    3. Save user message
    4. Run OpenAI Agent with full history
    5. MCP tools execute backend logic and update DB
    6. Save assistant reply
    7. Return final response
    """
    user_id = current_user.user_id

    # Verify ownership and load conversation
    conversation = ChatService.get_conversation(
        session=session,
        conversation_id=conversation_id,
        user_id=user_id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "conversation_not_found", "message": f"Conversation {conversation_id} not found"}
        )

    # Save user message
    ChatService.save_message(
        session=session,
        conversation_id=conversation_id,
        role=MessageRole.USER,
        content=message.content
    )

    # Update conversation title from first message if default
    if conversation.title == "New Conversation":
        title = message.content[:50] + ("..." if len(message.content) > 50 else "")
        ChatService.update_conversation_title(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id,
            title=title
        )

    # Load conversation history for agent
    history = ChatService.load_history(session=session, conversation_id=conversation_id)
    openai_history = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history[:-1]  # Exclude current user message
    ]

    # Run agent with MCP tools
    try:
        agent = get_agent_service()
        response_text, tool_messages = agent.run(
            session=session,
            user_id=user_id,
            user_message=message.content,
            conversation_history=openai_history
        )
    except ValueError as e:
        logger.error(f"Agent configuration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "agent_configuration_error", "message": "AI service is not properly configured"}
        )
    except Exception as e:
        error_str = str(e)
        logger.error(f"Agent error: {e}")
        
        # Check for quota exceeded error
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "api_quota_exceeded",
                    "message": "AI service quota has been exceeded. Please try again later or contact support.",
                    "details": "The Gemini API free tier quota has been reached. Upgrade your plan or wait for quota reset."
                }
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "agent_error", "message": "Failed to process your request"}
        )

    # Save tool messages and assistant response
    for tool_msg in tool_messages:
        ChatService.save_message(
            session=session,
            conversation_id=conversation_id,
            role=MessageRole.TOOL,
            content=f"Tool: {tool_msg['tool_name']}",
            extra_data=tool_msg
        )

    ChatService.save_message(
        session=session,
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
        content=response_text
    )

    # Return response with updated messages
    all_messages = ChatService.load_history(session=session, conversation_id=conversation_id)

    logger.info(f"Chat response for user={user_id}, conv={conversation_id}")

    return {
        "response": response_text,
        "conversation_id": conversation_id,
        "messages": [msg.model_dump() for msg in all_messages]
    }


@router.post(
    "/message",
    response_model=dict,
    summary="Quick chat (auto-creates conversation)",
    description="Send a message without specifying a conversation. Creates a new conversation automatically.",
)
async def quick_chat(
    message: ChatMessageRequest,
    session: Session = Depends(get_session),
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> dict:
    """Quick chat endpoint that auto-creates a conversation."""
    # Create new conversation
    conversation = ChatService.create_conversation(
        session=session,
        user_id=current_user.user_id,
        title=message.content[:50] + ("..." if len(message.content) > 50 else "")
    )

    # Save user message
    ChatService.save_message(
        session=session,
        conversation_id=conversation.id,
        role=MessageRole.USER,
        content=message.content
    )

    # Run agent
    try:
        agent = get_agent_service()
        response_text, tool_messages = agent.run(
            session=session,
            user_id=current_user.user_id,
            user_message=message.content,
            conversation_history=[]
        )
    except Exception as e:
        error_str = str(e)
        logger.error(f"Agent error: {e}")
        
        # Check for quota exceeded error
        if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "quota" in error_str.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "api_quota_exceeded",
                    "message": "AI service quota has been exceeded. Please try again later or contact support.",
                    "details": "The Gemini API free tier quota has been reached. Upgrade your plan or wait for quota reset."
                }
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "agent_error", "message": "Failed to process your request"}
        )

    # Save tool messages and assistant response
    for tool_msg in tool_messages:
        ChatService.save_message(
            session=session,
            conversation_id=conversation.id,
            role=MessageRole.TOOL,
            content=f"Tool: {tool_msg['tool_name']}",
            extra_data=tool_msg
        )

    ChatService.save_message(
        session=session,
        conversation_id=conversation.id,
        role=MessageRole.ASSISTANT,
        content=response_text
    )

    # Load final messages
    all_messages = ChatService.load_history(session=session, conversation_id=conversation.id)

    return {
        "response": response_text,
        "conversation_id": conversation.id,
        "messages": [msg.model_dump() for msg in all_messages]
    }


__all__ = ["router"]
