# Tasks: Todo AI Chatbot
**Feature**: 1-todo-ai-chatbot
**Total Tasks**: 28 + 5 (Frontend)
**MVP Scope**: Phase 1-3 (US1: Add task via chat - foundational + test)
**Status**: Backend complete, Frontend UI complete, pending tests & migration

## Dependencies
- US1 → US2 (list after add)
- US2 → US3/US4/US5 (list for reference IDs)
- US6 after all (persistence test)

## Parallel Opportunities
- [P] Model creation (T002,T003)
- [P] Tests per story

## Phase 1: Setup
- [x] T001 Add OpenAI Agents SDK and MCP Python SDK to backend/requirements.txt

## Phase 2: Foundational (DB, Services, Agent, API)
- [x] T002 Create Conversation model per data-model.md in backend/src/models/conversation.py (user_id str index=True, no FK, nullable=False)
- [x] T003 Create Message model per data-model.md in backend/src/models/message.py (bidirectional rel, indexes, nullable=False)
- [x] T004 Generate Alembic migration for Conversation/Message in alembic/versions/003_add_chat_models.py
- [x] T005 Implement ChatService CRUD (create_conv, get_history) in backend/src/services/chat_service.py
- [x] T006 Implement MCP tools (add_task, list_tasks, update_task, complete_task, delete_task wrapping TaskService) in backend/src/services/agent_service.py
- [x] T007 Configure OpenAI Agent SDK (system prompt, bind MCP tools) in backend/src/services/agent_service.py
- [x] T008 Create chat router with JWT dep (get_current_user) in backend/src/routers/chat.py (POST /conversations, POST /{conv_id}/messages)
- [x] T009 Integrate memory load/save + agent run in chat endpoint backend/src/routers/chat.py

## Phase 3: US1 - Add new task via chat (P1)
- [ ] T010 [US1] Add minimal integration test for \"Add task buy milk\" → new task created (tests/integration/test_chat_add.py)
- [ ] T011 [US1] Refine add_task MCP tool validation/error handling in backend/src/services/agent_service.py

## Phase 4: US2 - List tasks via chat (P1)
- [ ] T012 [US2] Add minimal test for \"Show pending tasks\" → list returned (tests/integration/test_chat_list.py)
- [ ] T013 [US2] Enhance list_tasks tool (status filter) in backend/src/services/agent_service.py

## Phase 5: US3 - Update task via chat (P2)
- [ ] T014 [US3] Add minimal test for \"Change task 1 title\" → updated (tests/integration/test_chat_update.py)
- [ ] T015 [US3] Refine update_task MCP tool in backend/src/services/agent_service.py

## Phase 6: US4 - Complete task via chat (P2)
- [ ] T016 [US4] Add minimal test for \"Mark task 2 complete\" → status changed (tests/integration/test_chat_complete.py)
- [ ] T017 [US4] Implement complete_task MCP tool toggle in backend/src/services/agent_service.py

## Phase 7: US5 - Delete task via chat (P2)
- [ ] T018 [US5] Add minimal test for \"Delete task 3\" → removed (tests/integration/test_chat_delete.py)
- [ ] T019 [US5] Implement delete_task MCP tool in backend/src/services/agent_service.py

## Phase 8: US6 - Persistent conversations (P3)
- [ ] T020 [US6] Add persistence test: Create conv, restart, history loads (tests/integration/test_chat_persistence.py)

## Phase 9: Polish & Cross-Cutting
- [x] T021 [P] Add schemas (ChatMessage, ConversationResponse) in backend/src/models/conversation.py and message.py (inline)
- [x] T022 [P] Add error handling (invalid ID, auth fail) in chat router backend/src/routers/chat.py
- [x] T023 [P] Add ownership validation in all MCP tools backend/src/services/agent_service.py
- [ ] T024 [P] Unit tests for ChatService backend/tests/services/test_chat_service.py
- [ ] T025 [P] Unit tests for MCP tools backend/tests/services/test_agent_service.py
- [x] T026 Add app.include_router(chat) in backend/src/main.py
- [ ] T027 Run Alembic upgrade head
- [ ] T028 E2E smoke test all AC phrases via curl/HTTPie

## Phase 10: Frontend UI (Added)
- [x] T029 Add chat types and API methods to frontend/src/lib/api.ts
- [x] T030 Create ChatMessage component in frontend/src/components/chatbot/ChatMessage.tsx
- [x] T031 Create ChatInput component in frontend/src/components/chatbot/ChatInput.tsx
- [x] T032 Create ConversationList component in frontend/src/components/chatbot/ConversationList.tsx
- [x] T033 Create ChatWindow component in frontend/src/components/chatbot/ChatWindow.tsx
- [x] T034 Create ChatButton (floating) in frontend/src/components/chatbot/ChatButton.tsx
- [x] T035 Add ChatButton to layout.tsx for global access
- [x] T036 Create dedicated /chat page in frontend/src/app/chat/page.tsx

## Backend Reorganization (Completed)
- [x] T037 Move chatbot files to backend/src/chatbot/ package (models.py, services.py, router.py)
- [x] T038 Update imports in main.py and alembic/env.py