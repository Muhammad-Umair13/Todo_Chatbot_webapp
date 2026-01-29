# Tasks: Full-Stack Multi-User Web Todo Application

**Input**: Design documents from `/specs/002-todo-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Constitution Principle III mandates TDD. All implementation tasks include corresponding test tasks that MUST be written first and FAIL before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Monorepo structure (from plan.md):
- **Backend**: `apps/api/src/`, `apps/api/tests/`
- **Frontend**: `apps/web/src/`, `apps/web/tests/`
- **Shared**: `packages/types/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Monorepo initialization and basic structure

- [X] T001 Initialize monorepo root with pnpm workspace configuration in pnpm-workspace.yaml
- [X] T002 Create Turborepo configuration in turbo.json with dev, build, test, lint pipelines
- [X] T003 [P] Create root package.json with workspace scripts and dev dependencies
- [X] T004 [P] Initialize Git with .gitignore for Node.js, Python, and environment files
- [X] T005 Create apps/ directory for web and api applications
- [X] T006 Create packages/ directory for shared types and configs

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T007 Initialize FastAPI project structure in apps/api/ with pyproject.toml (Poetry)
- [X] T008 [P] Create apps/api/src/ directory structure (models, schemas, routers, services, auth, core)
- [ ] T009 [P] Create apps/api/tests/ directory structure (unit, integration, contract, conftest.py)
- [X] T010 Configure FastAPI application in apps/api/src/main.py with CORS and middleware
- [X] T011 [P] Create database connection module in apps/api/src/database.py with SQLModel engine
- [X] T012 [P] Configure Pydantic Settings in apps/api/src/core/config.py for environment variables
- [X] T013 [P] Create security utilities in apps/api/src/core/security.py (error handlers, validators)
- [X] T014 Setup Alembic for database migrations in apps/api/alembic/
- [X] T015 [P] Create pytest fixtures in apps/api/tests/conftest.py (test database, test client)
- [X] T016 [P] Create .env.example template in apps/api/ with all required environment variables

### Frontend Foundation

- [X] T017 Initialize Next.js 16+ project in apps/web/ with TypeScript and App Router
- [X] T018 [P] Configure Tailwind CSS in apps/web/tailwind.config.js
- [X] T019 [P] Configure TypeScript in apps/web/tsconfig.json with strict mode
- [X] T020 [P] Create apps/web/src/app/ directory structure (auth and dashboard route groups)
- [X] T021 [P] Create apps/web/src/components/ directory structure (auth, tasks, ui, providers)
- [X] T022 [P] Create apps/web/src/lib/ for utilities (api-client.ts, auth.ts, validation.ts)
- [X] T023 [P] Create apps/web/src/hooks/ for custom hooks (useAuth.ts, useTasks.ts)
- [ ] T024 [P] Setup Jest and React Testing Library in apps/web/jest.config.js
- [ ] T025 [P] Create .env.local.example template in apps/web/

### Shared Packages

- [ ] T026 [P] Create packages/types package with API TypeScript definitions in packages/types/api-types.ts
- [ ] T027 [P] Create packages/config/eslint-config with shared ESLint rules
- [ ] T028 [P] Create packages/config/typescript-config with shared TypeScript base config

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, log in with JWT tokens, refresh tokens, and log out securely

**Independent Test**: Register new account with email/password → login → receive JWT tokens → validate token works → logout

**Spec Reference**: spec.md lines 10-25 (User Story 1), FR-001 to FR-008
**Plan Reference**: plan.md Authentication Flow section, data-model.md User entity

### Tests for User Story 1 (TDD - Write First) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T029 [P] [US1] Write contract test for POST /auth/register in apps/api/tests/contract/test_auth_api.py
- [ ] T030 [P] [US1] Write contract test for POST /auth/login in apps/api/tests/contract/test_auth_api.py
- [ ] T031 [P] [US1] Write contract test for POST /auth/refresh in apps/api/tests/contract/test_auth_api.py
- [ ] T032 [P] [US1] Write contract test for POST /auth/logout in apps/api/tests/contract/test_auth_api.py
- [ ] T033 [P] [US1] Write unit test for password hashing in apps/api/tests/unit/test_password_utils.py
- [ ] T034 [P] [US1] Write unit test for JWT token generation in apps/api/tests/unit/test_jwt_utils.py
- [ ] T035 [P] [US1] Write integration test for user registration flow in apps/api/tests/integration/test_auth_flow.py
- [ ] T036 [P] [US1] Write component test for Login form in apps/web/tests/components/auth/LoginForm.test.tsx
- [ ] T037 [P] [US1] Write component test for Signup form in apps/web/tests/components/auth/SignupForm.test.tsx

**Verification**: Run `pytest apps/api/tests/` and `pnpm test --filter=web` - ALL tests should FAIL (Red)

### Backend Implementation for User Story 1

- [ ] T038 [P] [US1] Create User SQLModel in apps/api/src/models/user.py with email, hashed_password, name fields
- [ ] T039 [P] [US1] Create User Pydantic schemas in apps/api/src/schemas/auth.py (RegisterRequest, LoginRequest, AuthResponse)
- [ ] T040 [P] [US1] Create password hashing utilities in apps/api/src/auth/password.py using passlib with bcrypt
- [ ] T041 [P] [US1] Create JWT utilities in apps/api/src/auth/jwt.py (create_access_token, create_refresh_token, verify_token)
- [ ] T042 [US1] Create AuthService in apps/api/src/services/auth_service.py (register_user, authenticate_user, refresh_token_service)
- [ ] T043 [US1] Create authentication middleware in apps/api/src/auth/dependencies.py (get_current_user dependency)
- [ ] T044 [US1] Implement POST /auth/register endpoint in apps/api/src/routers/auth.py
- [ ] T045 [US1] Implement POST /auth/login endpoint in apps/api/src/routers/auth.py
- [ ] T046 [US1] Implement POST /auth/refresh endpoint in apps/api/src/routers/auth.py
- [ ] T047 [US1] Implement POST /auth/logout endpoint in apps/api/src/routers/auth.py
- [ ] T048 [US1] Create initial Alembic migration for users table in apps/api/alembic/versions/
- [ ] T049 [US1] Apply database migration with `alembic upgrade head`

**Verification**: Run `pytest apps/api/tests/` - ALL User Story 1 tests should PASS (Green)

### Frontend Implementation for User Story 1

- [ ] T050 [P] [US1] Create AuthContext provider in apps/web/src/components/providers/AuthProvider.tsx
- [ ] T051 [P] [US1] Create useAuth hook in apps/web/src/hooks/useAuth.ts
- [ ] T052 [P] [US1] Create API client for auth in apps/web/src/lib/api-client.ts (register, login, refresh, logout functions)
- [ ] T053 [P] [US1] Create auth utilities in apps/web/src/lib/auth.ts (token storage, validation)
- [ ] T054 [P] [US1] Create form validation utilities in apps/web/src/lib/validation.ts
- [ ] T055 [US1] Create Login form component in apps/web/src/components/auth/LoginForm.tsx
- [ ] T056 [US1] Create Signup form component in apps/web/src/components/auth/SignupForm.tsx
- [ ] T057 [US1] Create login page in apps/web/src/app/(auth)/login/page.tsx
- [ ] T058 [US1] Create signup page in apps/web/src/app/(auth)/signup/page.tsx
- [ ] T059 [US1] Create auth layout in apps/web/src/app/(auth)/layout.tsx
- [ ] T060 [US1] Create protected dashboard layout with auth check in apps/web/src/app/(dashboard)/layout.tsx

**Verification**: Run `pnpm test --filter=web` - ALL User Story 1 tests should PASS (Green)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can register, login, and access protected routes.

---

## Phase 4: User Story 2 - Create and View Personal Tasks (Priority: P2)

**Goal**: Authenticated users can create new tasks with title/description/priority/due_date and view their personal task list with user data isolation

**Independent Test**: Login → create task with title → view task list → verify task appears → logout → login as different user → verify cannot see first user's tasks

**Spec Reference**: spec.md lines 28-43 (User Story 2), FR-009 to FR-013
**Plan Reference**: data-model.md Task entity, contracts/tasks.yaml GET/POST /tasks

### Tests for User Story 2 (TDD - Write First) ⚠️

- [ ] T061 [P] [US2] Write contract test for POST /tasks (create) in apps/api/tests/contract/test_tasks_api.py
- [ ] T062 [P] [US2] Write contract test for GET /tasks (list) in apps/api/tests/contract/test_tasks_api.py
- [ ] T063 [P] [US2] Write contract test for GET /tasks/{id} (retrieve) in apps/api/tests/contract/test_tasks_api.py
- [ ] T064 [P] [US2] Write unit test for TaskService.create_task in apps/api/tests/unit/test_task_service.py
- [ ] T065 [P] [US2] Write unit test for TaskService.get_user_tasks in apps/api/tests/unit/test_task_service.py
- [ ] T066 [P] [US2] Write integration test for user data isolation in apps/api/tests/integration/test_user_isolation.py
- [ ] T067 [P] [US2] Write component test for TaskForm in apps/web/tests/components/tasks/TaskForm.test.tsx
- [ ] T068 [P] [US2] Write component test for TaskList in apps/web/tests/components/tasks/TaskList.test.tsx

**Verification**: Run tests - ALL should FAIL (Red)

### Backend Implementation for User Story 2

- [ ] T069 [P] [US2] Create Task SQLModel in apps/api/src/models/task.py with user_id FK, title, description, completed, priority, due_date
- [ ] T070 [P] [US2] Create Task Pydantic schemas in apps/api/src/schemas/task.py (CreateTaskRequest, TaskResponse)
- [ ] T071 [US2] Create TaskService in apps/api/src/services/task_service.py (create_task, get_user_tasks, get_task_by_id)
- [ ] T072 [US2] Implement POST /tasks endpoint in apps/api/src/routers/tasks.py with ownership assignment
- [ ] T073 [US2] Implement GET /tasks endpoint in apps/api/src/routers/tasks.py with user_id filtering
- [ ] T074 [US2] Implement GET /tasks/{id} endpoint in apps/api/src/routers/tasks.py with ownership validation
- [ ] T075 [US2] Create Alembic migration for tasks table in apps/api/alembic/versions/
- [ ] T076 [US2] Apply migration with `alembic upgrade head`

**Verification**: Run `pytest apps/api/tests/` - User Story 2 tests should PASS (Green)

### Frontend Implementation for User Story 2

- [ ] T077 [P] [US2] Create useTasks hook in apps/web/src/hooks/useTasks.ts
- [ ] T078 [P] [US2] Create API client for tasks in apps/web/src/lib/api-client.ts (createTask, getTasks, getTask functions)
- [ ] T079 [P] [US2] Define Task TypeScript types in packages/types/api-types.ts
- [ ] T080 [US2] Create TaskForm component in apps/web/src/components/tasks/TaskForm.tsx
- [ ] T081 [US2] Create TaskCard component in apps/web/src/components/tasks/TaskCard.tsx
- [ ] T082 [US2] Create TaskList component in apps/web/src/components/tasks/TaskList.tsx
- [ ] T083 [US2] Create EmptyState component in apps/web/src/components/ui/EmptyState.tsx
- [ ] T084 [US2] Create tasks page in apps/web/src/app/(dashboard)/tasks/page.tsx

**Verification**: Run `pnpm test --filter=web` - User Story 2 tests should PASS (Green)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can register, login, create tasks, and view their own tasks only.

---

## Phase 5: User Story 3 - Update and Complete Tasks (Priority: P3)

**Goal**: Authenticated users can update task fields (title, description, priority, due_date) and toggle completion status with ownership validation

**Independent Test**: Login → create task → update task fields → verify changes saved → mark complete → verify status changed → toggle back to incomplete → verify status changed

**Spec Reference**: spec.md lines 46-61 (User Story 3), FR-014, FR-015, FR-017
**Plan Reference**: contracts/tasks.yaml PUT /tasks/{id}, PATCH /tasks/{id}/complete

### Tests for User Story 3 (TDD - Write First) ⚠️

- [ ] T085 [P] [US3] Write contract test for PUT /tasks/{id} (update) in apps/api/tests/contract/test_tasks_api.py
- [ ] T086 [P] [US3] Write contract test for PATCH /tasks/{id}/complete in apps/api/tests/contract/test_tasks_api.py
- [ ] T087 [P] [US3] Write unit test for TaskService.update_task in apps/api/tests/unit/test_task_service.py
- [ ] T088 [P] [US3] Write unit test for TaskService.toggle_completion in apps/api/tests/unit/test_task_service.py
- [ ] T089 [P] [US3] Write integration test for ownership validation (403 errors) in apps/api/tests/integration/test_ownership_validation.py
- [ ] T090 [P] [US3] Write component test for TaskEditForm in apps/web/tests/components/tasks/TaskEditForm.test.tsx

**Verification**: Run tests - ALL should FAIL (Red)

### Backend Implementation for User Story 3

- [ ] T091 [P] [US3] Create UpdateTaskRequest schema in apps/api/src/schemas/task.py
- [ ] T092 [US3] Add update_task method to TaskService in apps/api/src/services/task_service.py with ownership check
- [ ] T093 [US3] Add toggle_completion method to TaskService in apps/api/src/services/task_service.py
- [ ] T094 [US3] Implement PUT /tasks/{id} endpoint in apps/api/src/routers/tasks.py with 403/404 handling
- [ ] T095 [US3] Implement PATCH /tasks/{id}/complete endpoint in apps/api/src/routers/tasks.py

**Verification**: Run `pytest apps/api/tests/` - User Story 3 tests should PASS (Green)

### Frontend Implementation for User Story 3

- [ ] T096 [P] [US3] Add updateTask and toggleComplete functions to apps/web/src/lib/api-client.ts
- [ ] T097 [US3] Create TaskEditForm component in apps/web/src/components/tasks/TaskEditForm.tsx
- [ ] T098 [US3] Add edit functionality to TaskCard component in apps/web/src/components/tasks/TaskCard.tsx
- [ ] T099 [US3] Add completion toggle to TaskCard component in apps/web/src/components/tasks/TaskCard.tsx

**Verification**: Run `pnpm test --filter=web` - User Story 3 tests should PASS (Green)

**Checkpoint**: All user stories 1, 2, AND 3 should now be independently functional. Full task lifecycle management is complete.

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Authenticated users can permanently delete tasks they own with ownership validation

**Independent Test**: Login → create task → delete task → verify task no longer in list → attempt to delete another user's task → verify 403 error

**Spec Reference**: spec.md lines 64-79 (User Story 4), FR-016
**Plan Reference**: contracts/tasks.yaml DELETE /tasks/{id}

### Tests for User Story 4 (TDD - Write First) ⚠️

- [ ] T100 [P] [US4] Write contract test for DELETE /tasks/{id} in apps/api/tests/contract/test_tasks_api.py
- [ ] T101 [P] [US4] Write unit test for TaskService.delete_task in apps/api/tests/unit/test_task_service.py
- [ ] T102 [P] [US4] Write integration test for delete with ownership validation in apps/api/tests/integration/test_task_deletion.py

**Verification**: Run tests - ALL should FAIL (Red)

### Implementation for User Story 4

- [ ] T103 [US4] Add delete_task method to TaskService in apps/api/src/services/task_service.py with ownership check
- [ ] T104 [US4] Implement DELETE /tasks/{id} endpoint in apps/api/src/routers/tasks.py with 204/403/404 responses
- [ ] T105 [US4] Add deleteTask function to apps/web/src/lib/api-client.ts
- [ ] T106 [US4] Add delete button with confirmation to TaskCard in apps/web/src/components/tasks/TaskCard.tsx

**Verification**: Run tests - User Story 4 tests should PASS (Green)

**Checkpoint**: All 4 user stories should now be independently functional. Complete CRUD operations available.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T107 [P] Create loading spinner component in apps/web/src/components/ui/LoadingSpinner.tsx
- [ ] T108 [P] Create error boundary component in apps/web/src/components/providers/ErrorBoundary.tsx
- [ ] T109 [P] Create toast notification system in apps/web/src/components/ui/Toast.tsx
- [ ] T110 [P] Add error logging to backend in apps/api/src/core/logging.py
- [ ] T111 [P] Configure structured error responses in apps/api/src/core/error_handlers.py
- [ ] T112 [P] Add loading states to all async operations in apps/web/src/components/tasks/
- [ ] T113 [P] Add error handling to all API calls in apps/web/src/lib/api-client.ts
- [ ] T114 [P] Create landing page in apps/web/src/app/page.tsx
- [ ] T115 [P] Configure CORS properly in apps/api/src/main.py
- [ ] T116 [P] Setup OpenAPI documentation route /docs in apps/api/src/main.py
- [ ] T117 [P] Add filtering by completion status to GET /tasks endpoint
- [ ] T118 [P] Add sorting options to TaskList component
- [ ] T119 [P] Create README.md in repository root with setup instructions
- [ ] T120 Validate quickstart.md instructions work end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories ✅ MVP
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Requires User model from US1
- **User Story 3 (P3)**: Can start after User Story 2 - Extends Task CRUD
- **User Story 4 (P4)**: Can start after User Story 2 - Completes Task CRUD

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Backend before frontend (or parallel if contract defined)
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup phase**: T003, T004, T006 can run in parallel
- **Foundational phase**: Many tasks marked [P] can run in parallel
  - Backend setup (T008, T009, T011, T012, T013, T015, T016)
  - Frontend setup (T018, T019, T021, T022, T023, T024, T025)
  - Package setup (T026, T027, T028)
- **User Story tests**: All tests for a story marked [P] can run in parallel
- **User Story models/schemas**: Tasks marked [P] within a story can run in parallel
- **Different user stories**: Can be worked on in parallel by different team members after Foundational

---

## Parallel Example: User Story 1

```bash
# Phase 1: Write all tests in parallel (Red)
Task T029: Contract test POST /auth/register
Task T030: Contract test POST /auth/login
Task T031: Contract test POST /auth/refresh
Task T032: Contract test POST /auth/logout
Task T033: Unit test password hashing
Task T034: Unit test JWT generation
Task T035: Integration test registration flow
Task T036: Component test Login form
Task T037: Component test Signup form

# Phase 2: Implement models and utilities in parallel
Task T038: User SQLModel
Task T039: Auth Pydantic schemas
Task T040: Password hashing utilities
Task T041: JWT utilities

# Phase 3: Implement services and endpoints sequentially
Task T042: AuthService (depends on T038-T041)
Task T043: Auth middleware (depends on T041, T042)
Task T044-T047: Auth endpoints (depend on T042, T043)

# Phase 4: Database migration
Task T048-T049: Alembic migration (depends on T038)

# Phase 5: Frontend components in parallel
Task T050-T054: Auth infrastructure (can be parallel)
Task T055-T060: Auth UI components (depends on T050-T054)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP Deliverable**: Users can register, login, and access protected routes with JWT authentication.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) ✅
3. Add User Story 2 → Test independently → Deploy/Demo (Task creation)
4. Add User Story 3 → Test independently → Deploy/Demo (Task updates)
5. Add User Story 4 → Test independently → Deploy/Demo (Task deletion)
6. Add Polish → Final release

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Task CRUD) - waits for US1 User model
   - Developer C: Polish tasks (can start some UI components)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **TDD MANDATORY**: Verify tests fail before implementing (Red-Green-Refactor)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Run `pytest` and `pnpm test` frequently during development
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 120

**Breakdown by Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 22 tasks
- Phase 3 (User Story 1): 33 tasks (9 tests + 24 implementation)
- Phase 4 (User Story 2): 24 tasks (8 tests + 16 implementation)
- Phase 5 (User Story 3): 15 tasks (6 tests + 9 implementation)
- Phase 6 (User Story 4): 7 tasks (3 tests + 4 implementation)
- Phase 7 (Polish): 14 tasks

**Test Tasks**: 26 (TDD requirement)
**Parallel Opportunities**: 45 tasks marked [P]

**MVP Scope**: Phases 1-3 (61 tasks) delivers authentication system

**Full Feature**: All phases (120 tasks) delivers complete todo application with authentication and full CRUD

---

**Ready for Implementation**: Execute with `/sp.implement` or start manually with Phase 1 Setup tasks
