"""Chatbot services for Phase III AI Chatbot.

Contains:
- ChatService: Conversation and message CRUD operations
- MCPTools: MCP tools layer wrapping TaskService (only DB access layer)
- AgentService: Google Gemini with function calling

Architecture (per plan.md):
    Agent ≠ Database
    MCP tools = only layer allowed to touch the database
"""

import json
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Optional, List, Any

from sqlmodel import Session, select
from google import genai
from google.genai import types
from loguru import logger

from ..models.task import TaskCreate, TaskUpdate, TaskResponse
from ..services.task_service import TaskService
from .models import (
    Conversation,
    ConversationResponse,
    Message,
    MessageRole,
    MessageResponse,
)


# ============================================================================
# Chat Service - Conversation/Message CRUD
# ============================================================================

class ChatService:
    """Service class for handling chat conversation and message operations.

    All methods are stateless - state is loaded/saved from/to DB per request.
    user_id must come from JWT, never from frontend input.
    """

    MAX_HISTORY_MESSAGES = 20

    @staticmethod
    def create_conversation(
        session: Session,
        user_id: str,
        title: Optional[str] = None
    ) -> ConversationResponse:
        """Create a new conversation for the specified user."""
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation",
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        logger.info(f"Created conversation id={conversation.id}, user_id={user_id}")

        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            message_count=0,
        )

    @staticmethod
    def get_conversation(
        session: Session,
        conversation_id: int,
        user_id: str
    ) -> Optional[ConversationResponse]:
        """Get a specific conversation by ID for the specified user."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            logger.warning(f"Conversation not found: id={conversation_id}, user_id={user_id}")
            return None

        msg_statement = select(Message).where(Message.conversation_id == conversation_id)
        message_count = len(session.exec(msg_statement).all())

        return ConversationResponse(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            message_count=message_count,
        )

    @staticmethod
    def list_conversations(
        session: Session,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[ConversationResponse]:
        """List all conversations for the specified user."""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        conversations = session.exec(statement).all()

        results = []
        for conv in conversations:
            msg_statement = select(Message).where(Message.conversation_id == conv.id)
            message_count = len(session.exec(msg_statement).all())

            results.append(ConversationResponse(
                id=conv.id,
                user_id=conv.user_id,
                title=conv.title,
                created_at=conv.created_at,
                message_count=message_count,
            ))

        return results

    @staticmethod
    def save_message(
        session: Session,
        conversation_id: int,
        role: MessageRole,
        content: str,
        extra_data: Optional[dict] = None
    ) -> MessageResponse:
        """Save a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            extra_data=extra_data,
        )
        session.add(message)
        session.commit()
        session.refresh(message)

        logger.debug(f"Saved message id={message.id}, conv={conversation_id}, role={role.value}")

        return MessageResponse(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            extra_data=message.extra_data,
            created_at=message.created_at,
        )

    @staticmethod
    def load_history(
        session: Session,
        conversation_id: int,
        limit: Optional[int] = None
    ) -> List[MessageResponse]:
        """Load message history for a conversation."""
        max_messages = limit or ChatService.MAX_HISTORY_MESSAGES

        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(max_messages)
        )
        messages = session.exec(statement).all()
        messages = list(reversed(messages))

        return [
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                extra_data=msg.extra_data,
                created_at=msg.created_at,
            )
            for msg in messages
        ]

    @staticmethod
    def get_or_create_conversation(
        session: Session,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> ConversationResponse:
        """Get existing conversation or create a new one."""
        if conversation_id:
            conv = ChatService.get_conversation(session, conversation_id, user_id)
            if conv:
                return conv
            logger.warning(f"Conversation {conversation_id} not found, creating new")

        return ChatService.create_conversation(session, user_id)

    @staticmethod
    def update_conversation_title(
        session: Session,
        conversation_id: int,
        user_id: str,
        title: str
    ) -> Optional[ConversationResponse]:
        """Update conversation title."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return None

        conversation.title = title[:255]
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

        return ChatService.get_conversation(session, conversation_id, user_id)

    @staticmethod
    def delete_conversation(
        session: Session,
        conversation_id: int,
        user_id: str
    ) -> bool:
        """Delete a conversation and all its messages."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()

        if not conversation:
            return False

        session.delete(conversation)
        session.commit()
        logger.info(f"Deleted conversation id={conversation_id}")

        return True


# ============================================================================
# MCP Tools - Only Layer Allowed to Access Database
# ============================================================================

@dataclass
class ToolResult:
    """Result from an MCP tool execution."""
    success: bool
    data: Any
    error: Optional[str] = None


class MCPTools:
    """MCP tools layer - the ONLY layer allowed to access the database.

    All tools receive user_id from JWT (passed by router) to enforce ownership.
    Tools wrap TaskService methods and format results for the agent.
    """

    @staticmethod
    def add_task(
        session: Session,
        user_id: str,
        title: str,
        description: str = ""
    ) -> ToolResult:
        """Add a new task for the user."""
        try:
            if not title or not title.strip():
                return ToolResult(success=False, data=None, error="Task title is required")

            task_data = TaskCreate(
                title=title.strip(),
                description=description.strip() if description else "",
            )
            task = TaskService.create_task(session, task_data, user_id)

            logger.info(f"MCP add_task: created task id={task.id} for user={user_id}")

            return ToolResult(
                success=True,
                data={
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                }
            )
        except Exception as e:
            logger.error(f"MCP add_task error: {e}")
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def list_tasks(
        session: Session,
        user_id: str,
        status: Optional[str] = None
    ) -> ToolResult:
        """List tasks for the user with optional status filter."""
        try:
            completed = None
            if status == "pending":
                completed = False
            elif status == "completed":
                completed = True

            tasks = TaskService.get_tasks(session, user_id, completed=completed)

            logger.info(f"MCP list_tasks: found {len(tasks)} tasks for user={user_id}")

            return ToolResult(
                success=True,
                data={
                    "tasks": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "description": t.description,
                            "completed": t.completed,
                        }
                        for t in tasks
                    ],
                    "total": len(tasks),
                    "filter": status or "all",
                }
            )
        except Exception as e:
            logger.error(f"MCP list_tasks error: {e}")
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def update_task(
        session: Session,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> ToolResult:
        """Update task details."""
        try:
            update_data = TaskUpdate()
            if title is not None:
                update_data.title = title.strip()
            if description is not None:
                update_data.description = description.strip()

            task = TaskService.update_task(session, task_id, user_id, update_data)

            if not task:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Task {task_id} not found or you don't have permission"
                )

            logger.info(f"MCP update_task: updated task id={task_id}")

            return ToolResult(
                success=True,
                data={
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                }
            )
        except Exception as e:
            logger.error(f"MCP update_task error: {e}")
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def complete_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> ToolResult:
        """Mark a task as completed."""
        try:
            update_data = TaskUpdate(completed=True)
            task = TaskService.update_task(session, task_id, user_id, update_data)

            if not task:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Task {task_id} not found or you don't have permission"
                )

            logger.info(f"MCP complete_task: completed task id={task_id}")

            return ToolResult(
                success=True,
                data={
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed,
                    "message": f"Task '{task.title}' marked as completed"
                }
            )
        except Exception as e:
            logger.error(f"MCP complete_task error: {e}")
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def delete_task(
        session: Session,
        user_id: str,
        task_id: int
    ) -> ToolResult:
        """Delete a task by ID."""
        try:
            task = TaskService.get_task_by_id(session, task_id, user_id)
            if not task:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"Task {task_id} not found or you don't have permission"
                )

            task_title = task.title
            deleted = TaskService.delete_task(session, task_id, user_id)

            if not deleted:
                return ToolResult(success=False, data=None, error=f"Failed to delete task {task_id}")

            logger.info(f"MCP delete_task: deleted task id={task_id}")

            return ToolResult(
                success=True,
                data={
                    "id": task_id,
                    "title": task_title,
                    "message": f"Task '{task_title}' has been deleted"
                }
            )
        except Exception as e:
            logger.error(f"MCP delete_task error: {e}")
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def delete_task_by_name(
        session: Session,
        user_id: str,
        task_name: str
    ) -> ToolResult:
        """Delete a task by name/title (case-insensitive partial match)."""
        try:
            # Get all tasks for the user
            tasks = TaskService.get_tasks(session, user_id)

            # Find tasks matching the name (case-insensitive)
            task_name_lower = task_name.lower().strip()
            matching_tasks = [
                t for t in tasks
                if task_name_lower in t.title.lower()
            ]

            if not matching_tasks:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"No task found matching '{task_name}'"
                )

            if len(matching_tasks) > 1:
                # Multiple matches - return list for user to choose
                task_list = ", ".join([f"'{t.title}' (ID: {t.id})" for t in matching_tasks])
                return ToolResult(
                    success=False,
                    data={"matching_tasks": [{"id": t.id, "title": t.title} for t in matching_tasks]},
                    error=f"Multiple tasks match '{task_name}': {task_list}. Please specify which one to delete by using the exact name or ID."
                )

            # Single match - delete it
            task = matching_tasks[0]
            task_id = task.id
            task_title = task.title
            deleted = TaskService.delete_task(session, task_id, user_id)

            if not deleted:
                return ToolResult(success=False, data=None, error=f"Failed to delete task '{task_title}'")

            logger.info(f"MCP delete_task_by_name: deleted task id={task_id} title='{task_title}'")

            return ToolResult(
                success=True,
                data={
                    "id": task_id,
                    "title": task_title,
                    "message": f"Task '{task_title}' has been deleted"
                }
            )
        except Exception as e:
            logger.error(f"MCP delete_task_by_name error: {e}")
            return ToolResult(success=False, data=None, error=str(e))

    @staticmethod
    def complete_task_by_name(
        session: Session,
        user_id: str,
        task_name: str
    ) -> ToolResult:
        """Mark a task as completed by name/title (case-insensitive partial match)."""
        try:
            # Get all tasks for the user
            tasks = TaskService.get_tasks(session, user_id)

            # Find tasks matching the name (case-insensitive)
            task_name_lower = task_name.lower().strip()
            matching_tasks = [
                t for t in tasks
                if task_name_lower in t.title.lower() and not t.completed
            ]

            if not matching_tasks:
                return ToolResult(
                    success=False,
                    data=None,
                    error=f"No pending task found matching '{task_name}'"
                )

            if len(matching_tasks) > 1:
                # Multiple matches - return list for user to choose
                task_list = ", ".join([f"'{t.title}' (ID: {t.id})" for t in matching_tasks])
                return ToolResult(
                    success=False,
                    data={"matching_tasks": [{"id": t.id, "title": t.title} for t in matching_tasks]},
                    error=f"Multiple tasks match '{task_name}': {task_list}. Please specify which one to complete."
                )

            # Single match - complete it
            task = matching_tasks[0]
            update_data = TaskUpdate(completed=True)
            updated_task = TaskService.update_task(session, task.id, user_id, update_data)

            if not updated_task:
                return ToolResult(success=False, data=None, error=f"Failed to complete task '{task.title}'")

            logger.info(f"MCP complete_task_by_name: completed task id={task.id} title='{task.title}'")

            return ToolResult(
                success=True,
                data={
                    "id": task.id,
                    "title": task.title,
                    "completed": True,
                    "message": f"Task '{task.title}' marked as completed"
                }
            )
        except Exception as e:
            logger.error(f"MCP complete_task_by_name error: {e}")
            return ToolResult(success=False, data=None, error=str(e))


# ============================================================================
# Agent Service - Google Gemini with Function Calling (new google-genai SDK)
# ============================================================================

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo tasks through natural language conversation.

## Capabilities
You can help users:
- Add new tasks (provide a title and optional description)
- List their tasks (all, pending, or completed)
- Update task details (title, description)
- Mark tasks as complete (by ID or by name)
- Delete tasks (by ID or by name)

## Rules
1. ALWAYS use the provided tools for task operations. Never invent or guess task IDs.
2. After each action, confirm what was done in natural language.
3. If the user's intent is unclear, ask a clarifying question.
4. Be concise, professional, and helpful.
5. When listing tasks, present them clearly with IDs for reference.
6. If a task is not found, inform the user politely.
7. When users refer to tasks by name, use the *_by_name tools (delete_task_by_name, complete_task_by_name).
8. When users refer to tasks by ID, use the ID-based tools (delete_task, complete_task).

## Examples
- "Add a task to buy milk" → use add_task tool
- "Show my pending tasks" → use list_tasks with status="pending"
- "Mark task 2 as complete" → use complete_task with task_id=2
- "Complete the buy groceries task" → use complete_task_by_name with task_name="buy groceries"
- "Delete task 3" → use delete_task with task_id=3
- "Delete the buy milk task" → use delete_task_by_name with task_name="buy milk"
- "Change task 1 title to buy eggs" → use update_task with task_id=1, title="buy eggs"
"""


# Define tools for Gemini
def _get_tool_declarations():
    """Get function declarations for Gemini tools."""
    return [
        types.FunctionDeclaration(
            name="add_task",
            description="Add a new task for the user",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "title": types.Schema(type=types.Type.STRING, description="The task title (required)"),
                    "description": types.Schema(type=types.Type.STRING, description="Optional task description"),
                },
                required=["title"],
            ),
        ),
        types.FunctionDeclaration(
            name="list_tasks",
            description="List tasks for the user with optional status filter",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "status": types.Schema(
                        type=types.Type.STRING,
                        description="Filter by status: 'pending', 'completed', or 'all'",
                        enum=["pending", "completed", "all"],
                    ),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="update_task",
            description="Update task details (title and/or description)",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="ID of the task to update"),
                    "title": types.Schema(type=types.Type.STRING, description="New task title"),
                    "description": types.Schema(type=types.Type.STRING, description="New task description"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="complete_task",
            description="Mark a task as completed",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="ID of the task to complete"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="delete_task",
            description="Delete a task by ID",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_id": types.Schema(type=types.Type.INTEGER, description="ID of the task to delete"),
                },
                required=["task_id"],
            ),
        ),
        types.FunctionDeclaration(
            name="delete_task_by_name",
            description="Delete a task by its name/title. Use this when the user refers to a task by name instead of ID.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_name": types.Schema(type=types.Type.STRING, description="Name/title of the task to delete (partial match supported)"),
                },
                required=["task_name"],
            ),
        ),
        types.FunctionDeclaration(
            name="complete_task_by_name",
            description="Mark a task as completed by its name/title. Use this when the user refers to a task by name instead of ID.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "task_name": types.Schema(type=types.Type.STRING, description="Name/title of the task to complete (partial match supported)"),
                },
                required=["task_name"],
            ),
        ),
    ]


class AgentService:
    """Gemini Agent service for natural language task management.

    Flow: User message → Agent (reasoning) → Tool call → MCPTools → TaskService → DB
    """

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model
        self.system_prompt = SYSTEM_PROMPT
        self.tools = [types.Tool(function_declarations=_get_tool_declarations())]

    def _execute_tool(
        self,
        session: Session,
        user_id: str,
        tool_name: str,
        tool_args: dict
    ) -> ToolResult:
        """Execute an MCP tool by name."""
        tool_map = {
            "add_task": MCPTools.add_task,
            "list_tasks": MCPTools.list_tasks,
            "update_task": MCPTools.update_task,
            "complete_task": MCPTools.complete_task,
            "delete_task": MCPTools.delete_task,
            "delete_task_by_name": MCPTools.delete_task_by_name,
            "complete_task_by_name": MCPTools.complete_task_by_name,
        }

        tool_func = tool_map.get(tool_name)
        if not tool_func:
            return ToolResult(success=False, data=None, error=f"Unknown tool: {tool_name}")

        # Convert task_id from string to int if needed
        if "task_id" in tool_args and isinstance(tool_args["task_id"], str):
            tool_args["task_id"] = int(tool_args["task_id"])

        return tool_func(session, user_id, **tool_args)

    def run(
        self,
        session: Session,
        user_id: str,
        user_message: str,
        conversation_history: List[dict]
    ) -> tuple[str, List[dict]]:
        """Run the agent with user message and conversation history."""

        # Build chat history for Gemini
        contents = []

        # Add conversation history
        for msg in conversation_history:
            role = "user" if msg.get("role") == "user" else "model"
            contents.append(types.Content(
                role=role,
                parts=[types.Part.from_text(text=msg.get("content", ""))]
            ))

        # Add current user message
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)]
        ))

        tool_messages = []
        max_iterations = 5

        # Generate config with tools
        config = types.GenerateContentConfig(
            system_instruction=self.system_prompt,
            tools=self.tools,
        )

        for iteration in range(max_iterations):
            logger.debug(f"Agent iteration {iteration + 1}")

            try:
                # Call Gemini
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config,
                )
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Gemini API Error: {error_msg}")
                
                # Re-raise with more context for outer handler
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    logger.error("API Quota Exceeded - Free tier limit reached")
                    raise RuntimeError(f"Gemini API quota exceeded: {error_msg}")
                
                raise

            if not response.candidates or not response.candidates[0].content.parts:
                break

            # Add model response to history
            contents.append(response.candidates[0].content)

            has_function_call = False
            function_responses = []

            for part in response.candidates[0].content.parts:
                if part.function_call:
                    has_function_call = True
                    fc = part.function_call
                    tool_name = fc.name
                    tool_args = dict(fc.args) if fc.args else {}

                    logger.info(f"Agent calling tool: {tool_name} with args: {tool_args}")

                    # Execute the tool
                    result = self._execute_tool(session, user_id, tool_name, tool_args)

                    # Track tool call
                    tool_messages.append({
                        "tool_name": tool_name,
                        "tool_args": tool_args,
                        "tool_result": result.data if result.success else {"error": result.error},
                        "success": result.success
                    })

                    # Prepare function response part
                    # Note: The google-genai SDK expects a dictionary in 'response'
                    function_responses.append(types.Part.from_function_response(
                        name=tool_name,
                        response={"result": result.data} if result.success else {"error": result.error}
                    ))

            if has_function_call:
                # Add function responses as a single message from the 'tool' (or 'user' depending on SDK version)
                # In current SDK, function responses are often passed back as 'user' role but with function_response parts
                contents.append(types.Content(
                    role="user",
                    parts=function_responses
                ))
                continue
            else:
                # No more function calls, we have a text response
                if response.text:
                    logger.info(f"Agent response: {response.text[:100]}...")
                    return response.text, tool_messages
                break

        # Final response
        final_text = response.text if response.text else "I processed your request."
        logger.info(f"Agent final response: {final_text[:100]}...")
        return final_text, tool_messages


def get_agent_service() -> AgentService:
    """Factory function to create AgentService with config."""
    from ..core.config import get_settings
    import os

    settings = get_settings()
    api_key = getattr(settings, 'gemini_api_key', None) or os.getenv('GEMINI_API_KEY')

    if not api_key:
        raise ValueError("GEMINI_API_KEY not configured. Add GEMINI_API_KEY to your .env file.")

    model = getattr(settings, 'gemini_model', 'gemini-2.0-flash')
    return AgentService(api_key=api_key, model=model)


__all__ = [
    "ChatService",
    "MCPTools",
    "ToolResult",
    "AgentService",
    "get_agent_service",
    "SYSTEM_PROMPT",
]
