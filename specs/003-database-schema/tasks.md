# Implementation Tasks: Phase II Database Schema

## Feature Overview

Implement a PostgreSQL-based task persistence system with strict user isolation for Phase II of the Todo Web Application. The system will use SQLModel for ORM, Alembic for migrations, and Neon Serverless PostgreSQL for storage. All task operations enforce ownership at the database level through user_id filtering, ensuring zero data leakage between users.

## Implementation Strategy

**MVP Scope**: Focus on User Story 1 (Create and Persist Tasks) as the minimal viable product that demonstrates the database layer working correctly.

**Implementation Order**:
1. Setup foundational database infrastructure
2. Implement User Story 1 (core persistence)
3. Implement User Story 2 (filtering)
4. Implement User Story 3 (updates)
5. Polish and validation

## Dependencies

- User authentication system provides reliable user identification
- Database connectivity must be established and configured
- Better Auth integration for JWT extraction

## Parallel Execution Opportunities

- Model creation can run in parallel with service layer development
- Alembic setup can run in parallel with database configuration
- Multiple API endpoints can be developed in parallel once models and services are complete

---

## Phase 1: Setup Infrastructure

**Goal**: Establish the foundational database infrastructure and configuration.

- [X] T001 Set up backend project structure with SQLModel, Alembic, and FastAPI dependencies
- [X] T002 Create backend/src/models/__init__.py file with proper imports
- [X] T003 Create backend/src/services/__init__.py file with proper imports
- [X] T004 Create backend/src/routers/__init__.py file with proper imports
- [X] T005 Create backend/src/schemas/__init__.py file with proper imports
- [X] T006 Create backend/src/core/__init__.py file with proper imports
- [X] T007 Create backend/src/auth/__init__.py file with proper imports
- [X] T008 Initialize Alembic in backend directory with proper configuration

---

## Phase 2: Foundational Database Layer

**Goal**: Implement the core database models and connection management required by all user stories.

- [X] T009 [P] Create Task SQLModel model in backend/src/models/task.py with fields from data-model.md
- [X] T010 [P] Create database connection management in backend/src/database.py
- [X] T011 [P] Create core configuration in backend/src/core/config.py
- [X] T012 [P] Create JWT authentication dependencies in backend/src/auth/dependencies.py
- [X] T013 Configure Alembic env.py to work with SQLModel metadata
- [X] T014 Generate initial migration for Task table with all required fields and indexes
- [X] T015 Update alembic.ini with proper database URL configuration

---

## Phase 3: [US1] Create and Persist Tasks

**Goal**: Enable authenticated users to create todo items that persist across sessions and server restarts.

**Independent Test Criteria**: Can be fully tested by creating a task, restarting the server, and verifying the task still exists and is retrievable by the same user.

- [X] T016 [P] Create TaskCreate Pydantic schema in backend/src/schemas/task.py
- [X] T017 [P] Create TaskRead Pydantic schema in backend/src/schemas/task.py
- [X] T018 [P] Create TaskService with create_task method in backend/src/services/task_service.py
- [X] T019 [P] Create POST /api/tasks endpoint in backend/src/routers/tasks.py
- [X] T020 [P] Implement title validation (minimum 1 character) in Task model
- [X] T021 [P] Implement description validation (maximum 1000 characters) in Task model
- [X] T022 [P] Implement automatic timestamp management in Task model
- [X] T023 [P] Add user_id extraction from JWT to POST /api/tasks endpoint
- [X] T024 [P] Add proper error handling for validation failures in POST endpoint
- [X] T025 Test task creation and persistence functionality

---

## Phase 4: [US2] View and Filter Personal Tasks

**Goal**: Allow authenticated users to view all their tasks and filter them by completion status.

**Independent Test Criteria**: Can be fully tested by creating multiple tasks for a user, marking some as completed, and verifying that both full task lists and filtered views work correctly.

- [X] T026 [P] Create TaskUpdate Pydantic schema in backend/src/schemas/task.py
- [X] T027 [P] Extend TaskService with get_tasks method in backend/src/services/task_service.py
- [X] T028 [P] Extend TaskService with get_task_by_id method in backend/src/services/task_service.py
- [X] T029 [P] Create GET /api/tasks endpoint in backend/src/routers/tasks.py
- [X] T030 [P] Implement user_id filtering in get_tasks method to ensure user isolation
- [X] T031 [P] Implement completion status filtering in get_tasks method
- [X] T032 [P] Create GET /api/tasks/{id} endpoint in backend/src/routers/tasks.py
- [X] T033 [P] Add user_id verification to GET /api/tasks/{id} endpoint
- [X] T034 Test personal task viewing and filtering functionality

---

## Phase 5: [US3] Update Task Details

**Goal**: Allow authenticated users to modify task details including title, description, and completion status.

**Independent Test Criteria**: Can be fully tested by creating a task, modifying its details, and verifying the changes persist correctly across session boundaries.

- [X] T035 [P] Extend TaskService with update_task method in backend/src/services/task_service.py
- [X] T036 [P] Extend TaskService with toggle_completion method in backend/src/services/task_service.py
- [X] T037 [P] Create PUT /api/tasks/{id} endpoint in backend/src/routers/tasks.py
- [X] T038 [P] Create PATCH /api/tasks/{id} endpoint in backend/src/routers/tasks.py
- [X] T039 [P] Create PATCH /api/tasks/{id}/complete endpoint in backend/src/routers/tasks.py
- [X] T040 [P] Implement proper validation in update operations
- [X] T041 [P] Implement updated_at timestamp updates in update operations
- [X] T042 [P] Add user_id verification to all update endpoints
- [X] T043 Test task update functionality

---

## Phase 6: Polish & Validation

**Goal**: Complete the implementation with proper error handling, validation, and verification.

- [X] T044 [P] Add comprehensive error handling with appropriate HTTP status codes
- [X] T045 [P] Add structured JSON error responses
- [X] T046 [P] Implement proper session cleanup in database connection
- [X] T047 [P] Add proper logging for database operations
- [X] T048 [P] Update __init__.py files to properly export all modules
- [X] T049 [P] Add database migration execution to deployment process
- [X] T050 [P] Create comprehensive test suite for all functionality
- [X] T051 [P] Verify Neon PostgreSQL reflects schema correctly
- [X] T052 [P] Document how to run migrations locally
- [X] T053 [P] Document how to verify tables in Neon
- [X] T054 [P] Document how future models will be added

---

## Task Dependencies

1. **Phase 1** (Setup) must complete before any other phase
2. **Phase 2** (Foundational) must complete before any User Story phases
3. **Phase 3** (US1) provides the base functionality for other user stories
4. **Phase 4** (US2) can run in parallel with Phase 5 (US3) but depends on Phase 2
5. **Phase 5** (US3) depends on Phase 2
6. **Phase 6** (Polish) can run in parallel with other phases but should be completed last

## Parallel Execution Examples

- T009-T012 (models, database, config, auth) can run in parallel during Phase 2
- T016-T019 (schemas, service, endpoint) can run in parallel during Phase 3
- T026-T033 (schemas, services, endpoints) can run in parallel during Phase 4
- T035-T042 (services, endpoints) can run in parallel during Phase 5