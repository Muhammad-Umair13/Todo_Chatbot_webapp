---
id: 0006
title: Fix Date Prioritization in Parser
stage: green
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: Muhammad Umair
command: /sp.phr
labels: ["bug-fix", "date-parsing", "nlp"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - todo_apps/utils/date_parser.py
 - todo_apps/cli/menu.py
tests:
 - manual verification script
---

## Prompt

I face one more problem now, when I give date its apply by defualt date everytime not apply my date.Fix it : Enter due date (e.g. tomorrow, 2025-12-31): today, 2027-12-2
Make recurring? (Y/n): n

✓ Task added: "hi" (ID: 2)
Priority: 🟡 Medium  | Tags: None
Due: 2025-12-31 | Repeats: none

## Response snapshot

Improved date parsing logic to prevent "general" dates like 'today' from shadowing more specific dates in a multi-part input string. The parser now evaluates all segments and returns the most specific/latest valid date, ensuring user-defined dates are correctly applied.

## Outcome

- ✅ Impact: Users can now provide verbose input (e.g. "today, 2027-12-2") and have the specific date correctly recognized instead of defaulting to 'today'.
- 🧪 Tests: Manual verification script confirmed correct parsing of multi-segment dates.
- 📁 Files: Updated `todo_apps/utils/date_parser.py` and cleaned up `todo_apps/cli/menu.py`.
- 🔁 Next prompts: none.
- 🧠 Reflection: When parsing user input, shadowing (where one rule matches too early) is a common trap. Parsing all fragments and applying a priority heuristic is safer.

## Evaluation notes (flywheel)

- Failure modes observed: none.
- Graders run and results (PASS/FAIL): PASS.
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Add unit tests specifically for the date parser edge cases.
