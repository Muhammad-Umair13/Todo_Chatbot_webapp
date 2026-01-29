# Implementation Plan: Todo AI Chatbot

**Feature Branch**: `1-todo-ai-chatbot`
**Created**: 2026-01-24
**Status**: Draft

## Technical Context

Existing: FastAPI backend with SQLModel ORM (Neon PG), Better Auth JWT, Task CRUD (models/task.py, services/task_service.py).

New: OpenAI Agents SDK for NL intent → MCP tools → TaskService/DB. Stateless /api/chat endpoints. Conversation/Message models.

## Constitution Check

[From .specify/memory/constitution.md - principles aligned: SDD workflow, small changes, tests first, security (JWT ownership), no direct DB from agent.]

## Scope and Dependencies

**In Scope**:
- Natural language task management via chat.
- Persistent conversations.
- OpenAI Agents SDK + MCP tools.
- Stateless backend.

**Out of Scope**:
- Frontend UI.
- Multi-modal.

**Dependencies**:
- OpenAI API, existing DB/Auth.

## Key Decisions and Rationale

- **OpenAI Agents SDK**: Simplest for tools/memory. Trade-off: Vendor lock vs speed.
- **MCP Tools**: Wrapper funcs (list_tasks(user_id), etc.) → TaskService. Ensures agent no DB access.
- **Memory**: Load last 20 msgs/conv per user.
- **Stateless**: DB for all state.

**Folder Structure**:
```
backend/src/
├── models/ (conversation.py, message.py)
├── services/ (chat_service.py, agent_service.py)
├── routers/ (chat.py)
├── schemas/ (chat.py)
```

## Data Flow

1. POST /api/chat/{conv_id}/message (JWT → user_id).
2. Load/create conv, history (ChatService).
3. AgentService: History → OpenAI agent (MCP tools).
4. Agent calls MCP → TaskService → DB.
5. Save msgs (user/tool/assistant).
6. Return response.

## Interfaces / API Contracts

**Endpoints**:
- POST /conversations → {id, title}
- POST /{conv_id}/messages → {response}

**MCP Tools**:
- list_tasks(user_id) → list[dict]
- create_task(user_id, title, desc) → dict
- etc.

Errors: 401/404/422.

## NFRs

- p95 <3s.
- 99.5% uptime.
- Security: JWT + ownership checks.

## Data / Migration

**Models**:
- Conversation: id, user_id, title, created_at
- Message: id, conv_id, role, content, metadata

Alembic migration.

## Ops / Risks

Observability: Logs/metrics.
Risks: Hallucination (tool schemas), cost (token limits).

## DoD

- E2E tests for AC.
- 100% tool cov.

**Critical Files**:
- backend/src/models/task.py
- backend/src/services/task_service.py
- etc.

📋 Architectural decision detected: OpenAI Agents SDK + MCP layer. Run `/sp.adr todo-ai-chatbot-architecture`?