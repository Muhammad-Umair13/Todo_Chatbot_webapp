---
id: 0007
title: Handle Already Completed Tasks Gracefully
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: Muhammad Umair
command: /sp.phr
labels: ["bug-fix", "error-handling", "ux"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - todo_apps/cli/menu.py
tests:
 - manual test script
---

## Prompt

Now date is perfect. But only one problem which I see when I mark task 2 and again mark this task 2 (which is already marked) its give me error, but I want not give error jut tell me to already marked : Enter task ID to complete (required): 1
Traceback (most recent call last):
  ...
todo_apps.exceptions.TaskAlreadyCompletedError: Task 1 is already completed.

## Response snapshot

Implemented error handling for `TaskAlreadyCompletedError` in the interactive menu. Instead of crashing with a traceback, the CLI now displays a friendly yellow warning message letting the user know the task is already finished.

## Outcome

- ✅ Impact: Prevented application crashes when redundant actions are performed by users.
- 🧪 Tests: Mock-input script verified the yellow message display and successful recovery.
- 📁 Files: Updated `todo_apps/cli/menu.py`.
- 🔁 Next prompts: none.
- 🧠 Reflection: Domain exceptions like "AlreadyCompleted" should always be caught at the UI boundary to maintain a clean user experience.

## Evaluation notes (flywheel)

- Failure modes observed: none.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add similar handling for 'delete' if a user attempts to delete a non-existent task inside the wizard.
