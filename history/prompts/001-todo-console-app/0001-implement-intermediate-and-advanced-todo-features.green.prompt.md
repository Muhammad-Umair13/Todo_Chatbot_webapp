---
id: 0001
title: Implement Intermediate and Advanced Todo Features
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: Muhammad Umair
command: /sp.phr
labels: ["priority", "tags", "search", "filter", "sort", "recurrence", "nlp-dates"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - todo_apps/models/task.py
 - todo_apps/services/task_service.py
 - todo_apps/cli/parser.py
 - todo_apps/cli/commands.py
 - todo_apps/models/__init__.py
 - todo_apps/services/__init__.py
 - tests/unit/test_task.py
 - tests/unit/test_memory.py
 - tests/unit/test_task_service.py
 - tests/integration/test_cli.py
 - todo_apps/utils/__init__.py
 - todo_apps/utils/date_parser.py
tests:
 - tests/unit/test_task.py
 - tests/unit/test_memory.py
 - tests/unit/test_task_service.py
 - tests/integration/test_cli.py
---

## Prompt

Run todo-app-architecture agent and Improve this todo cli app according to given instruction : # TASK: Enhance Todo CLI App with Intermediate & Advanced Features

## CURRENT STATUS
We have a working Phase 1 Todo CLI app with:
- ✅ Add, Delete, Update, View, Mark Complete features
- ✅ In-memory storage with Python 3.13+
- ✅ Basic CLI interface with direct commands
- ✅ Spec-driven development completed

## ENHANCEMENT REQUIREMENTS
Add the following features to make the app "polished and practical":

### INTERMEDIATE LEVEL (Organization & Usability)
1. **Priorities & Tags/Categories**
   - Assign priority levels: high/medium/low
   - Add tags/categories: work, home, personal, etc.
   - Tasks can have multiple tags

2. **Search & Filter**
   - Search by keyword in title/description
   - Filter by: status (completed/pending), priority, tags, date range
   - Combine multiple filters

3. **Sort Tasks**
   - Sort by: due date, priority, created date, updated date, title (alphabetical)
   - Ascending/descending order
   - Multiple sort criteria (priority then due date)

### ADVANCED LEVEL (Intelligent Features)
4. **Recurring Tasks**
   - Auto-reschedule repeating tasks
   - Patterns: daily, weekly, monthly, custom (every X days)
   - On completion, create next instance automatically

5. **Due Dates & Time Reminders**
   - Set deadlines with date/time
   - Natural language parsing: "tomorrow 2pm", "next monday"
   - Reminder notifications (console alerts for now)
   - Timezone support

## CONSTRAINTS TO MAINTAIN
1. **Keep existing functionality** - All Phase 1 commands must still work
2. **Backward compatible** - Don't break existing user workflows
3. **CLI-first design** - All features accessible via command line
4. **In-memory storage** - Still no database (for Phase 1)
5. **Performance** - Maintain <100ms response time
6. **Clean architecture** - Follow existing patterns from Phase 1

## Response snapshot

Implemented comprehensive enhancements including priorities, tags, advanced search/filter/sort, recurring tasks, and natural language date parsing. Updated the core model, service, and CLI layers while ensuring all regression tests pass.

## Outcome

- ✅ Impact: Significantly increased the utility of the Todo application, enabling complex task management and automation.
- 🧪 Tests: 66 regression tests passed; manual validation performed for NL parsing and recurrence logic.
- 📁 Files: 12 files modified or created across models, services, cli, utils, and tests.
- 🔁 Next prompts: Implement persistent storage (SQLite) to make recurring tasks truly useful across sessions.
- 🧠 Reflection: Lightweight NL parsing is highly effective for CLI usability; automatic recurrence logic should be carefully isolated in the service layer.

## Evaluation notes (flywheel)

- Failure modes observed: Initial script execution failed due to environment mismatch (Win32 powershell vs bash).
- Graders run and results (PASS/FAIL): PHR creation fall-back PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add more complex NL patterns (e.g., "every 2 weeks") to the parser.
