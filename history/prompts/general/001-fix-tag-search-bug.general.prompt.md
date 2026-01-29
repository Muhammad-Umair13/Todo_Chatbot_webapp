---
id: 003
title: Fix Tag Search Bug in CLI and Menu
stage: green
date_iso: 2025-12-31
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-todo-console-app
user: User
command: null
labels: ["bug-fix", "cli", "tags", "ux"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - todo_apps/cli/menu.py
  - todo_apps/cli/commands.py
tests_yaml:
  - Manual verification of Option 6 in View Tasks menu
  - Case-insensitivity validation (HI vs hi)
---

# Prompt
I face one issue when I add task and add tags like "hi" and when I view task and select search by tags and when i write hi tag its not show me my task? fix it perfectly : Choose an option (1-5): 5
Enter keyword to search: hi
No tasks found matching your filters.

# Response
I've fixed the tag search bug by:
1. Adding a dedicated "Filter by Tag" option (Option 6) to the Interactive Menu.
2. Ensuring tags are correctly passed to the service layer.
3. Implementing consistent lowercase normalization in both `menu.py` and `commands.py` for case-insensitive searching.
Found that the "Search by Keyword" (Option 5) was being used for tag searches, which only searches titles and descriptions.
