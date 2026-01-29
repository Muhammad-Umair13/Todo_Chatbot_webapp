---
id: 4
title: Implement Phase III AI Chatbot
stage: green
date: 2026-01-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-ai-chatbot
branch: 1-todo-ai-chatbot
user: user
command: /sp.implement
labels: ["implementation","chatbot","mcp","openai","agent"]
links:
  spec: specs/1-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/requirements.txt
  - backend/src/models/conversation.py
  - backend/src/models/message.py
  - backend/src/models/__init__.py
  - backend/src/services/chat_service.py
  - backend/src/services/agent_service.py
  - backend/src/services/__init__.py
  - backend/src/routers/chat.py
  - backend/src/routers/__init__.py
  - backend/src/core/config.py
  - backend/src/main.py
  - backend/alembic/env.py
  - backend/alembic/versions/003_add_chat_models.py
tests: []

---

## Prompt

Implement Phase III chatbot according to the approved specifications, plan, and tasks.

Rules:
- Do not break Phase II features.
- Reuse existing CRUD where possible.
- MCP tools must call real backend logic.
- OpenAI Agent must only reason and choose tools.
- Backend must remain stateless.
- Store all chat messages in the database.
- user_id must always come from JWT.

Deliver:
- MCP server with task tools
- Agent setup with system prompt
- Chat API route
- Conversation & Message models
- CRUD utilities
- Example requests
- Inline documentation

## Response snapshot

Implemented complete Phase III AI Chatbot:
1. Added openai>=1.51.3, mcp>=1.0.0 to requirements.txt
2. Created Conversation model with user_id index, title, timestamps
3. Created Message model with role enum (user/assistant/tool), FK to conversation, metadata JSON
4. Implemented ChatService (CRUD for conversations/messages, load_history)
5. Implemented MCPTools class wrapping TaskService (add/list/update/complete/delete_task)
6. Configured AgentService with OpenAI SDK (gpt-4o-mini), system prompt, function calling
7. Created chat router with JWT auth (POST /conversations, POST /{conv_id}/messages, GET endpoints)
8. Added Alembic migration 003_add_chat_models.py
9. Integrated chat router in main.py
10. Added OPENAI_API_KEY to config.py

Architecture enforced: Agent ≠ Database; MCP tools = only DB layer.

## Outcome

- ✅ Impact: Full AI chatbot functionality implemented; ready for testing.
- 🧪 Tests: Pending (T024, T025, T028).
- 📁 Files: 13 files created/modified (see above).
- 🔁 Next prompts: Run migrations, add tests, E2E smoke test.
- 🧠 Reflection: Reused TaskService via MCPTools; stateless design; JWT ownership enforced.

## Evaluation notes (flywheel)

- Failure modes observed: None during implementation.
- Graders run and results (PASS/FAIL): Not yet run.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add integration tests.
