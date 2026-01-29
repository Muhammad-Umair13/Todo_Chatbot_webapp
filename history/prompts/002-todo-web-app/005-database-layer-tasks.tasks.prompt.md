---
id: 006
title: database-layer-tasks-generation
stage: tasks
date: 2025-01-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-todo-web-app
branch: 002-todo-web-app
user: unknown
command: /sp.tasks
labels: ["database", "tasks", "implementation"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-todo-web-app/database/tasks.md
 - history/prompts/002-todo-web-app/005-database-layer-tasks.tasks.prompt.md
tests:
 - None created (planning phase)
---

## Prompt

You are operating under the Phase II Constitution.

INPUT FILES:
- specs/002-todo-web-app/database/schema.md
- specs/002-todo-web-app/database/plan.md

OBJECTIVE:
Generate an official executable task list for implementing the Phase II database layer.

Your tasks MUST decompose the plan into small, atomic, Claude-executable steps.
Tasks MUST include (but are not limited to):

1. SQLModel Model Creation
   - Create Task model
   - Field constraints
   - Ownership column
   - Timestamp behavior

2. Alembic Configuration
   - Initialize Alembic
   - Configure database URL binding
   - Configure SQLModel metadata target

3. Migration Generation
   - Autogenerate initial migration
   - Review migration for correctness
   - Include index creation
   - Enforce nullability and defaults

4. Migration Execution
   - Apply migration to Neon
   - Verify schema exists

5. Database Validation
   - Verify tables exist
   - Verify indexes exist
   - Verify persistence behavior

6. Test Enablement
   - Prepare test DB configuration
   - Ensure migrations run in tests

OUTPUT FORMAT:
Create:
specs/002-todo-web-app/database/tasks.md

Each task MUST include:

- Task ID
- Description
- Input files
- Expected outputs
- Validation steps
- Failure conditions
QUALITY RULES:
- Tasks must be independently executable
- Tasks must be testable
- Tasks must not mix responsibilities
- Tasks must not include API or frontend work
- Tasks must explicitly reference schema and plan

After listing tasks, include a final section:
"Execution Order & Completion Criteria"

## Response snapshot

Generated 20 executable tasks across 6 phases for Phase II database layer implementation:

**Phase 1 (Setup)**: 3 tasks - Project initialization, Python dependencies, configuration
**Phase 2 (Foundational)**: 5 tasks - Database connection, Alembic init, Task model, models init, event listener
**Phase 3 (Migration)**: 2 tasks - Autogenerate and review initial migration
**Phase 4 (Migration)**: 2 tasks - Apply migration to Neon, validate schema
**Phase 5 (Test)**: 2 tasks - Test conftest and migration tests
**Phase 6 (Validation)**: 6 tasks - Model fields, indexes, ownership, FastAPI integration, phase safety, Alembic workflow

Tasks scoped strictly to database layer - no API routes, no frontend, no auth logic.

## Outcome

- \u2705 Impact: Generated comprehensive task list enabling implementation of Phase II database layer with 20 executable tasks organized across 6 phases
- \ud83e\uddea Tests: No tests created (planning phase)
- \ud83d\udcc1 Files: Created specs/002-todo-web-app/database/tasks.md with 20 tasks
- \ud83d\udd01 Next prompts: Ready for /sp.implement or individual task execution
- \ud83e\udde0 Reflection: Tasks follow checklist format with [P] parallel markers, [Story] labels (none applicable - database layer only), explicit file paths, and strict scope constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All tasks follow template requirements, scope locked to database layer, explicit references to schema.md and plan.md
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): None
