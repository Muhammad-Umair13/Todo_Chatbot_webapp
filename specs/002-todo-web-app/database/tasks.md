# Tasks: 002-todo-web-app - Database Layer Implementation

**Input**: Design documents from `specs/002-todo-web-app/database/`
**Prerequisites**: [schema.md](./schema.md) (required), [plan.md](./plan.md) (required)
**Scope**: Database layer only - no API routes, no frontend, no auth logic

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and database framework setup

- [ ] T001 [P] Create backend directory structure per plan.md
  - **Input**: specs/002-todo-web-app/database/plan.md
  - **Description**: Create directory structure `backend/src/{models,database.py}` and `backend/alembic/{versions,env.py,script.py.mako}` per plan.md structure definition
  - **Expected outputs**: Directory tree created with all required folders
  - **Validation steps**: Verify directories exist with `ls backend/` and `ls backend/src/`
  - **Failure conditions**: Directory creation fails or structure doesn't match plan.md

- [ ] T002 [P] Initialize Python project with dependencies per plan.md
  - **Input**: specs/002-todo-web-app/database/plan.md
  - **Description**: Initialize Python project with `pyproject.toml` or `requirements.txt` including sqlmodel, alembic, fastapi dependencies per Constitution Principle II
  - **Expected outputs**: `backend/pyproject.toml` with sqlmodel, alembic, fastapi, pydantic v2
  - **Validation steps**: Verify `sqlmodel` and `alembic` in dependencies with `pip show` or `poetry show`
  - **Failure conditions**: Dependency installation fails or versions don't match Constitution

- [ ] T003 [P] Configure SQLModel logging and environment variables
  - **Input**: specs/002-todo-web-app/database/plan.md, Constitution Principle IX (security)
  - **Description**: Create `backend/src/core/config.py` with pydantic settings for DATABASE_URL (no secrets), configure structured logging per Constitution Principle IX
  - **Expected outputs**: `backend/src/core/config.py` with Settings class using pydantic_settings
  - **Validation steps**: Verify config loads DATABASE_URL from environment, verify no hardcoded secrets in code
  - **Failure conditions**: Config module fails to load environment variables or contains hardcoded secrets

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database infrastructure that MUST be complete before any model or migration work

**⚠️ CRITICAL**: No model or migration tasks can begin until this phase is complete

- [ ] T004 [P] Create database.py with SQLModel engine and session management
  - **Input**: specs/002-todo-web-app/database/plan.md - "Integration with FastAPI Infrastructure" section
  - **Description**: Create `backend/src/database.py` with SQLModel `create_engine()`, `get_session()` dependency for FastAPI, connection pooling configuration per plan.md
  - **Expected outputs**: `backend/src/database.py` with `engine`, `get_session()` function using `Session(engine)` as generator
  - **Validation steps**: Import module successfully, verify engine uses environment DATABASE_URL, verify session generator syntax
  - **Failure conditions**: Module import fails, database connection test fails, session generator has syntax errors

- [ ] T005 [P] Initialize Alembic with SQLModel metadata targeting
  - **Input**: specs/002-todo-web-app/database/plan.md - "Alembic Migration Strategy" section
  - **Description**: Run `alembic init backend/alembic` then configure `alembic.ini` and `alembic/env.py` to target SQLModel Task metadata per plan.md configuration details
  - **Expected outputs**: `backend/alembic/` directory with `versions/`, `env.py`, `script.py.mako`, `alembic.ini` configured with `sqlalchemy.url` and `target_metadata`
  - **Validation steps**: Run `alembic --help` to verify initialization, check `alembic.ini` contains correct paths
  - **Failure conditions**: Alembic init command fails, env.py cannot import models, alembic.ini has wrong paths

- [ ] T006 [P] Create SQLModel Task model per canonical specification
  - **Input**: specs/002-todo-web-app/database/schema.md - canonical Task model, specs/002-todo-web-app/database/plan.md - SQLModel design section
  - **Description**: Create `backend/src/models/task.py` with `Task(SQLModel, table=True)` class implementing canonical fields: id, user_id(str), title, description, completed(bool), created_at(datetime), updated_at(datetime) per Constitution Principle IV
  - **Expected outputs**: `backend/src/models/task.py` with Task class using Field() decorators, index on user_id, datetime.utcnow factories
  - **Validation steps**: Import Task model successfully, verify all canonical fields present, verify user_id is str type (not int), verify title/description validators
  - **Failure conditions**: Model import fails, missing canonical fields, user_id is wrong type, validators not working

- [ ] T007 [P] Create models __init__.py to expose Task model
  - **Input**: specs/002-todo-web-app/database/plan.md - project structure
  - **Description**: Create `backend/src/models/__init__.py` with `from src.models.task import Task` to make Task model importable by Alembic env.py and application code
  - **Expected outputs**: `backend/src/models/__init__.py` that imports Task class
  - **Validation steps**: Verify `from src.models.task import Task` works without errors, verify `Task` is available in `src.models` namespace
  - **Failure conditions**: Import fails, Task not exposed correctly

- [ ] T008 [P] Configure SQLAlchemy event listener for auto-updating updated_at timestamp
  - **Input**: specs/002-todo-web-app/database/plan.md - "Timestamp Behavior" section
  - **Description**: Add SQLAlchemy `before_update` event listener in `backend/src/models/task.py` or separate event module to automatically set `updated_at` to current UTC time on any UPDATE operation per plan.md
  - **Expected outputs**: `updated_at` field is automatically set to `datetime.utcnow()` on every task update
  - **Validation steps**: Create test task, update it, verify updated_at changed from created_at, verify timestamp is UTC
  - **Failure conditions**: Event listener not registered, updated_at doesn't auto-update, timezone mismatch

---

## Phase 3: Migration Generation and Validation

**Purpose**: Create initial schema migration for Task table with indexes

- [ ] T009 [P] Autogenerate initial migration for Task table
  - **Input**: specs/002-todo-web-app/database/plan.md - "Migration Workflow" section, specs/002-todo-web-app/database/schema.md - SQL schema
  - **Description**: Run `alembic revision --autogenerate -m "Initial Task table"` to generate migration file creating task table with all canonical fields, indexes on user_id and (user_id, completed) per plan.md index strategy
  - **Expected outputs**: `backend/alembic/versions/XXX_initial.py` with upgrade() creating task table, indexes, and downgrade() dropping them
  - **Validation steps**: Review generated migration file, verify task table schema matches canonical model, verify both indexes created, verify downgrade() exists
  - **Failure conditions**: Migration autogeneration fails, schema doesn't match canonical model, indexes missing, downgrade missing

- [ ] T010 [P] Review and correct autogenerated migration per requirements
  - **Input**: specs/002-todo-web-app/database/schema.md - canonical model, specs/002-todo-web-app/database/plan.md - index strategy
  - **Description**: Manually review `backend/alembic/versions/XXX_initial.py`, ensure user_id is VARCHAR(255) (no FK), ensure created_at/updated_at use TIMESTAMPTZ with server_default=sa.func.now(), ensure ix_task_user_id and ix_task_user_id_completed indexes are created per plan.md
  - **Expected outputs**: Corrected migration file matching plan.md specifications exactly, no unintended changes, both upgrade and downgrade paths valid
  - **Validation steps**: Compare migration columns to canonical model, verify index statements match plan.md, check for raw SQL (should use op.*), verify no unintended tables or columns
  - **Failure conditions**: Migration has schema errors, missing indexes, contains FK constraint on user_id, has raw SQL instead of op.*, downgrade not reversible

---

## Phase 4: Migration Execution

**Purpose**: Apply migration to database and verify schema

- [ ] T011 [P] Apply migration to Neon PostgreSQL database
  - **Input**: specs/002-todo-web-app/database/plan.md - "Migration Workflow" section
  - **Description**: Run `alembic upgrade head` to apply initial migration to Neon database, verify task table and indexes are created per plan.md migration commands
  - **Expected outputs**: Migration applied successfully, task table exists in database, indexes exist (ix_task_user_id, ix_task_user_id_completed)
  - **Validation steps**: Run `alembic current` to verify migration applied, connect to database and query information_schema to verify table exists, check indexes with `SELECT * FROM pg_indexes WHERE tablename='task'`
  - **Failure conditions**: Migration command fails, table not created, indexes not created, database connection errors

- [ ] T012 [P] Validate schema exists in database with canonical structure
  - **Input**: specs/002-todo-web-app/database/schema.md - canonical model
  - **Description**: Connect to Neon database and verify task table has all required columns (id SERIAL, user_id VARCHAR(255) NOT NULL, title VARCHAR(200) NOT NULL, description TEXT DEFAULT '', completed BOOLEAN DEFAULT false, created_at TIMESTAMPTZ NOT NULL, updated_at TIMESTAMPTZ NOT NULL) and both indexes exist
  - **Expected outputs**: Database schema validated, all constraints confirmed, indexes confirmed functional
  - **Validation steps**: Query `\d task` in PostgreSQL, verify column types and constraints, verify indexes with `\di+`, test query performance with EXPLAIN
  - **Failure conditions**: Table missing columns, wrong column types, indexes not created, constraints violated

---

## Phase 5: Test Enablement

**Purpose**: Configure test database and ensure migrations can run in test environment

- [ ] T013 [P] Configure test database connection in tests/conftest.py
  - **Input**: specs/002-todo-web-app/database/plan.md - "Integration with FastAPI Infrastructure" section
  - **Description**: Create `backend/tests/conftest.py` with test session fixture using in-memory SQLite for fast tests, test DATABASE_URL override, setup and teardown per plan.md
  - **Expected outputs**: `backend/tests/conftest.py` with `test_session()` fixture using SQLite in-memory, SQLModel.metadata.create_all() for schema
  - **Validation steps**: Run `pytest tests/ -v` to verify fixtures load, test session creates tables, teardown cleans up properly
  - **Failure conditions**: Conftest import fails, fixture not found, session lifecycle issues

- [ ] T014 [P] Verify migrations run in test environment
  - **Input**: specs/002-todo-web-app/database/plan.md - "Migration Workflow" section
  - **Description**: Create test that verifies Alembic migrations can run in test environment, upgrades create schema, downgrades clean up per plan.md migration commands
  - **Expected outputs**: Test passes confirming migrations work in SQLite test environment
  - **Validation steps**: Run `pytest tests/ -k test_migration` to verify migration works, check tables created and dropped correctly
  - **Failure conditions**: Migration fails in test environment, schema mismatch between test and production migrations

---

## Phase 6: Database Validation

**Purpose**: Comprehensive validation of database layer implementation

- [ ] T015 [P] Verify task model fields match canonical specification exactly
  - **Input**: specs/002-todo-web-app/database/schema.md - canonical Task model
  - **Description**: Review `backend/src/models/task.py` and verify it has EXACTLY: id(int), user_id(str), title(str), description(str), completed(bool), created_at(datetime), updated_at(datetime) with correct Field decorators, index on user_id, datetime.utcnow factories
  - **Expected outputs**: Model validation report confirming all canonical fields present with correct types and constraints
  - **Validation steps**: Compare model fields to canonical schema one-by-one, verify Field() decorators match plan.md, check for any extra fields
  - **Failure conditions**: Missing canonical fields, wrong field types, extra fields present, wrong decorators

- [ ] T016 [P] Verify indexes are correctly created in migration
  - **Input**: specs/002-todo-web-app/database/plan.md - "Index Strategy" section
  - **Description**: Review migration file and verify ix_task_user_id (single) and ix_task_user_id_completed (composite) indexes are created using op.create_index(), verify no other indexes exist
  - **Expected outputs**: Index validation confirming both required indexes present, no extra indexes created
  - **Validation steps**: Read migration file, extract all op.create_index() calls, verify they match plan.md index names and columns
  - **Failure conditions**: Missing ix_task_user_id, missing ix_task_user_id_completed, extra indexes created, wrong column names

- [ ] T017 [P] Verify ownership enforcement at application level
  - **Input**: specs/002-todo-web-app/database/schema.md - "Data Isolation Strategy" section, Constitution Principle VIII
  - **Description**: Verify Task model and database setup support ownership queries, ensure there's NO foreign key constraint on user_id, application will filter by user_id in all operations
  - **Expected outputs**: Ownership validation confirming string user_id with index, no FK constraint, clear pattern for query-level filtering
  - **Validation steps**: Check Task model user_id type, check migration for FK constraint, verify plan.md query examples use user_id filter
  - **Failure conditions**: user_id has FK constraint, user_id is wrong type, ownership filtering not documented

- [ ] T018 [P] Verify FastAPI session injection works correctly
  - **Input**: specs/002-todo-web-app/database/plan.md - "Integration with FastAPI Infrastructure" section
  - **Description**: Verify `get_session()` from database.py can be used as FastAPI Depends() injection, verify session lifecycle is managed (created and closed automatically per request), verify engine is singleton with connection pooling
  - **Expected outputs**: Session integration validation confirming FastAPI can inject sessions, lifecycle management verified
  - **Validation steps**: Review database.py get_session() implementation, verify it's a generator with `with Session(engine) as session:`, check that it yields session and cleans up after request
  - **Failure conditions**: get_session() doesn't use generator pattern, session not yielded correctly, manual session cleanup required

- [ ] T019 [P] Verify phase safety controls are in place
  - **Input**: specs/002-todo-web-app/database/plan.md - "Phase Safety Controls" section
  - **Description**: Review implementation and verify Task model has NO priority, NO due_date, NO tags fields (Phase III+ features), verify no User table exists, verify schema is locked to Phase II canonical model
  - **Expected outputs**: Phase safety validation confirming no Phase III fields present, model locked to Phase II scope
  - **Validation steps**: Search codebase for 'priority', 'due_date', 'tags' keywords, verify only task table exists, check no other tables created
  - **Failure conditions**: Phase III fields present, User table exists, extra tables created, schema not locked to canonical model

- [ ] T020 [P] Verify Alembic configuration and workflow
  - **Input**: specs/002-todo-web-app/database/plan.md - "Alembic Migration Strategy" section
  - **Description**: Verify alembic.ini points to correct versions directory, env.py imports Task metadata, autogenerate and upgrade/downgrade commands work per plan.md
  - **Expected outputs**: Alembic workflow validation confirming configuration is correct, migration commands work
  - **Validation steps**: Run `alembic current`, run `alembic history`, test autogenerate command, verify versions directory has migration file
  - **Failure conditions**: Alembic commands fail, env.py cannot import models, versions directory wrong path

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all other phases
- **Migration Generation (Phase 3)**: Depends on Foundational completion
- **Migration Execution (Phase 4)**: Depends on Migration Generation completion
- **Test Enablement (Phase 5)**: Depends on Migration Execution completion
- **Database Validation (Phase 6)**: Depends on Test Enablement completion

### Within Each Phase

- Phase 1 (Setup): All tasks marked [P] can run in parallel
- Phase 2 (Foundational): T004-T006 are sequential (database.py before Alembic before model), but T007-T008 can run in parallel after T006
- Phase 3 (Migration): T009 and T010 are sequential
- Phase 4 (Migration): T011 and T012 are sequential
- Phase 5 (Test): T013 and T014 can run in parallel
- Phase 6 (Validation): T015-T020 can run in parallel after all earlier phases complete

### Sequential Execution Flow

```
Phase 1 (Setup) → Parallelizable
  ├─ T001 [P] - Create directory structure
  ├─ T002 [P] - Initialize Python project
  └─ T003 [P] - Configure logging and env

Phase 2 (Foundational) → Sequential Dependencies
  ├─ T004 [ ] - Create database.py
  ├─ T005 [ ] - Initialize Alembic
  ├─ T006 [ ] - Create Task model
  └─ T007 [ ] - Create __init__.py
       └─ T008 [ ] - Configure event listener

Phase 3 (Migration) → Sequential
  ├─ T009 [ ] - Autogenerate migration
  └─ T010 [ ] - Review migration

Phase 4 (Migration) → Sequential
  ├─ T011 [ ] - Apply migration
  └─ T012 [ ] - Validate schema

Phase 5 (Test) → Parallelizable
  ├─ T013 [ ] - Configure test DB
  └─ T014 [ ] - Verify migrations work

Phase 6 (Validation) → Parallelizable
  ├─ T015 [ ] - Verify model fields
  ├─ T016 [ ] - Verify indexes
  ├─ T017 [ ] - Verify ownership
  ├─ T018 [ ] - Verify FastAPI integration
  ├─ T019 [ ] - Verify phase safety
  └─ T020 [ ] - Verify Alembic workflow
```

---

## Implementation Strategy

### Minimal Viable Delivery

1. **Phase 1 Complete** (Setup): Directory structure, dependencies, configuration
2. **Phase 2 Complete** (Foundational): database.py, Alembic, Task model
3. **Phase 3 Complete** (Migration): Initial migration created and reviewed
4. **Phase 4 Complete** (Migration): Schema applied to Neon database
5. **Phase 5 Complete** (Test): Test fixtures and migration test passes
6. **Phase 6 Complete** (Validation): All validation checks pass

**STOP and VALIDATE**: After Phase 6, database layer is complete and ready for API implementation

### Incremental Delivery

Each phase adds measurable value:
- **Phase 1**: Foundation for all subsequent work
- **Phase 2**: Database infrastructure ready
- **Phase 3**: Migration file ready for version control
- **Phase 4**: Actual database schema exists
- **Phase 5**: Development workflow enabled with tests
- **Phase 6**: Verified against all requirements

---

## Notes

- [P] tasks = different files, no dependencies
- Database layer ONLY - no API routes, no frontend, no auth logic
- All tasks explicitly reference schema.md and plan.md
- Canonical Task model from Constitution Principle IV strictly followed
- String user_id (no FK) for Better Auth JWT integration
- No Phase III features (priority, due_date, tags) included
- Each task is independently testable
- Ownership enforced at query level (Constitution Principle VIII)
- All migrations use SQLModel metadata and op.* operations
- SQLAlchemy event listener for auto-updating updated_at timestamps
- Alembic workflow follows Constitution Principle IV requirements
- SQLite in-memory for test environment (fast, no dependencies on Neon)
