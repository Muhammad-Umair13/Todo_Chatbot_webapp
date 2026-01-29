---
id: 0008
title: Sort Tasks by ID Ascending in View Menu
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: Muhammad Umair
command: /sp.phr
labels: ["ui-correction", "sorting", "ux"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - todo_apps/cli/menu.py
tests:
 - manual verification
---

## Prompt

Correct somethings for better, first when I view all tasks its give me like this : ID | Status | Priority | Due Date | Title
...
But I want rearrange top 1 and then down 2 and then down 3 and so on task view.

## Response snapshot

Updated the default sorting behavior in the "View Tasks" menu. The application now lists tasks in ascending order of their ID (1, 2, 3...) as requested, making the list easier to follow chronologically.

## Outcome

- ✅ Impact: Improved readability of the task list by aligning it with the user's preferred mental model (ID-based ordering).
- 🧪 Tests: regression test PASS.
- 📁 Files: Updated `todo_apps/cli/menu.py`.
- 🔁 Next prompts: none.
- 🧠 Reflection: While "Recently Added" is a common default for many apps, a simple numerical ID sort is often more intuitive for console-based todo lists.

## Evaluation notes (flywheel)

- Failure modes observed: none.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
