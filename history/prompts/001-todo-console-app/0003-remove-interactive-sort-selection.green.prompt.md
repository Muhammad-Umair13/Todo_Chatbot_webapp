---
id: 0003
title: Remove Interactive Sort Selection from View Menu
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: Muhammad Umair
command: /sp.phr
labels: ["ux-simplification", "interactive-menu", "cleanup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - todo_apps/cli/menu.py
tests:
 - tests/unit/test_task.py
---

## Prompt

My todo cli app working perfectly and fantastic but something want to remove. This sort by option I dont want just remove it.When I click view task and see all task its give me Sort by section I dont want this

## Response snapshot

Removed the interactive "Sort by" prompt from `run_view_tasks_menu` in `menu.py`. The application now automatically sorts tasks by most recently added by default, streamlining the user experience.

## Outcome

- ✅ Impact: Reduced friction in the task viewing workflow by removing an unnecessary selection step.
- 🧪 Tests: regression test PASS.
- 📁 Files: Updated `todo_apps/cli/menu.py`.
- 🔁 Next prompts: none.
- 🧠 Reflection: Defaulting to a sensible sort order (Recently Added) is often better for UX than forcing a choice every time.

## Evaluation notes (flywheel)

- Failure modes observed: none.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add a toggle in "Settings" to change the default sort behavior if users request it later.
