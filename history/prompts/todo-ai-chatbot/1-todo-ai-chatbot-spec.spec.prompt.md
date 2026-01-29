---
id: 1
title: Todo AI Chatbot Specification
stage: spec
date: 2026-01-24
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-ai-chatbot
branch: 1-todo-ai-chatbot
user: user
command: /sp.specify
labels: ["spec","chatbot","ai","todo"]
links:
  spec: specs/1-todo-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-todo-ai-chatbot/spec.md
  - specs/1-todo-ai-chatbot/checklists/requirements.md
tests: []

---

## Prompt

Feature: Phase III – Todo AI Chatbot

Context:
We already have a Todo Full-Stack application with:
- FastAPI backend
- Neon PostgreSQL
- SQLModel ORM
- JWT authentication (Better Auth)
- CRUD for tasks (Phase II)

Goal:
Upgrade the system into an AI-powered chatbot that allows users to manage todos using natural language.

Core Requirements:
- Users can chat with the app to add, list, update, complete, and delete tasks.
- The backend must be stateless.
- All chat history must be stored in the database.
- The AI must not access the database directly.
- All real actions must be executed through MCP tools.
- OpenAI Agents SDK must be used for reasoning and tool selection.
- MCP Python SDK must be used to expose backend functions as tools.

Architecture:
Chat UI → FastAPI /api/chat → OpenAI Agent → MCP tools → SQLModel → Neon DB

Data Models to Add:
Conversation:
- id, user_id, title, created_at

Message:
- id, conversation_id, role (user/assistant/tool), content, created_at

Action (Tool) Specification:
- add_task(title, description, user_id)
- list_tasks(user_id, status=None)
- update_task(task_id, title=None, description=None)
- complete_task(task_id)
- delete_task(task_id)

Agent Behavior Rules:
- Use MCP tools for all task operations.
- Confirm successful actions in natural language.
- Ask clarifying questions if user intent is unclear.
- Never invent task IDs.
- Be concise, professional, and helpful.

Chat Workflow Specification:
1. Verify JWT and extract user_id
2. Load conversation from DB
3. Save user message
4. Run OpenAI Agent with full history
5. Allow MCP tool calls
6. MCP tools execute backend logic and update DB
7. Save assistant reply
8. Return final response

Security Rules:
- user_id must come from JWT, not frontend input
- MCP tools must validate task ownership

Acceptance Criteria:
- “Add a task to buy milk”
- “Show my pending tasks”
- “Mark task 2 as complete”
- “Change task 1 title to buy eggs”
- “Delete task 3”
- Conversations persist after server restart
- Unauthorized access is blocked

## Response snapshot

Created spec.md with user stories for add/list/update/complete/delete tasks via chat, functional requirements, key entities (Conversation, Message, Task), measurable success criteria. Generated passing quality checklist. No clarifications needed. Ready for planning.

## Outcome

- ✅ Impact: Feature specification fully defined and validated; enables planning phase.
- 🧪 Tests: None run (spec phase).
- 📁 Files: specs/1-todo-ai-chatbot/spec.md, specs/1-todo-ai-chatbot/checklists/requirements.md
- 🔁 Next prompts: /sp.plan for architecture.
- 🧠 Reflection: Spec remains technology-agnostic; used provided acceptance criteria directly.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): All checklist items PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
