# CLI Command Contracts: Todo Console Application

## Command Overview

| Command | Description | Exit Code |
|---------|-------------|-----------|
| `todo add "title" [-d "desc"]` | Create a new task | 0 on success, 1 on error |
| `todo list [--completed]` | List all tasks | 0 |
| `todo complete <id>` | Mark task complete | 0 on success, 1 on error |
| `todo delete <id>` | Delete a task | 0 on success, 1 on error |
| `todo update <id> "title" [-d "desc"]` | Update task details | 0 on success, 1 on error |
| `todo --help` | Show global help | 0 |
| `todo <command> --help` | Show command help | 0 |

---

## Command: `todo add`

### Purpose
Create a new task with a title and optional description.

### Syntax
```
todo add "TITLE" [-d "DESCRIPTION"]
```

### Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | title | string | Yes | Task title (1-200 chars) |

### Options

| Short | Long | Type | Description |
|-------|------|------|-------------|
| `-d` | `--description` | string | Task description (max 1000 chars) |

### Examples

```bash
# Basic usage
todo add "Buy groceries"

# With description
todo add "Buy groceries" -d "Milk, eggs, bread"

# With quoted description
todo add "Finish report" --description "Complete Q4 analysis"
```

### Output (Success)
```
✓ Task created: [1] Buy groceries
```

### Output (Error - Empty Title)
```
Error: Title cannot be empty.
```

### Output (Error - Title Too Long)
```
Error: Title must be 200 characters or less.
```

### Output (Error - Description Too Long)
```
Error: Description must be 1000 characters or less.
```

### Exit Codes
- `0`: Task created successfully
- `1`: Validation error or unexpected error

---

## Command: `todo list`

### Purpose
Display all tasks or filter by completion status.

### Syntax
```
todo list [--completed | --pending]
```

### Options

| Short | Long | Description |
|-------|------|-------------|
| | `--completed` | Show only completed tasks |
| | `--pending` | Show only incomplete tasks |

### Examples

```bash
# List all tasks
todo list

# List completed tasks only
todo list --completed

# List pending tasks only
todo list --pending
```

### Output (With Tasks)
```
ID  | Status     | Title
----|------------|------------------
1   | [ ]        | Buy groceries
2   | [x]        | Finish report
```

### Output (Empty List)
```
No tasks found. Add your first task with: todo add "Task title"
```

### Output (Filtered - Completed)
```
ID  | Status     | Title
----|------------|------------------
2   | [x]        | Finish report
```

### Exit Codes
- `0`: Always (even if empty)

---

## Command: `todo complete`

### Purpose
Mark a task as completed.

### Syntax
```
todo complete <ID>
```

### Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | id | integer | Yes | Task ID to complete |

### Examples

```bash
# Complete a task
todo complete 1
```

### Output (Success)
```
✓ Task [1] marked as completed
```

### Output (Error - Not Found)
```
Error: Task 999 not found.
```

### Output (Error - Already Completed)
```
✓ Task [1] is already completed
```

### Exit Codes
- `0`: Task completed successfully
- `1`: Task not found or other error

---

## Command: `todo delete`

### Purpose
Delete a task from the list.

### Syntax
```
todo delete <ID>
```

### Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | id | integer | Yes | Task ID to delete |

### Examples

```bash
# Delete a task
todo delete 1
```

### Output (Success)
```
✓ Task [1] deleted
```

### Output (Error - Not Found)
```
Error: Task 999 not found.
```

### Exit Codes
- `0`: Task deleted successfully
- `1`: Task not found or other error

---

## Command: `todo update`

### Purpose
Update a task's title and/or description.

### Syntax
```
todo update <ID> "TITLE" [-d "DESCRIPTION"]
```

### Arguments

| Position | Name | Type | Required | Description |
|----------|------|------|----------|-------------|
| 1 | id | integer | Yes | Task ID to update |
| 2 | title | string | Yes | New task title (1-200 chars) |

### Options

| Short | Long | Type | Description |
|-------|------|------|-------------|
| `-d` | `--description` | string | New task description (max 1000 chars) |

### Examples

```bash
# Update title only
todo update 1 "New title"

# Update title and description
todo update 1 "New title" -d "New description"
```

### Output (Success)
```
✓ Task [1] updated
```

### Output (Error - Not Found)
```
Error: Task 999 not found.
```

### Output (Error - Empty Title)
```
Error: Title cannot be empty.
```

### Exit Codes
- `0`: Task updated successfully
- `1`: Validation error or task not found

---

## Global Options

| Option | Description |
|--------|-------------|
| `-h`, `--help` | Show global help message |
| `-v`, `--version` | Show version information |

### Help Output
```
usage: todo [-h] [--version] {add,list,complete,delete,update} ...

Manage your todo list

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

commands:
  {add,list,complete,delete,update}
    add                 Add a new task
    list                List all tasks
    complete            Mark a task as complete
    delete              Delete a task
    update              Update a task
```

---

## Error Handling Contract

### Standard Error Format
All errors MUST output to stderr in the following format:
```
Error: <clear, user-friendly message>
```

### Error Types

| Error Type | Message Pattern | Exit Code |
|------------|-----------------|-----------|
| Task not found | `Error: Task {id} not found.` | 1 |
| Empty title | `Error: Title cannot be empty.` | 1 |
| Title too long | `Error: Title must be {max} characters or less.` | 1 |
| Description too long | `Error: Description must be {max} characters or less.` | 1 |
| Invalid ID format | `Error: Invalid task ID: '{value}'` | 2 |
| Missing required arg | Shows argparse error | 2 |

---

## Output Format Specifications

### List Command Table Format

```
ID  | Status     | Title
----|------------|------------------
{n:>2} | [{status}] | {title}
```

Where:
- `n`: Task ID (right-aligned, 2 chars)
- `status`: ` ` (space) for incomplete, `x` for completed
- `title`: Task title (truncated to fit column if needed)

### Color Output (Optional)

When terminal supports ANSI colors:
- Green checkmark (`:white_check_mark:`) for success
- Red error indicator (`Error:`) for errors
- Yellow for warnings

Color output MUST be disabled when:
- `NO_COLOR` environment variable is set
- Output is piped to another command
- `--no-color` flag is implemented

---

## Session Behavior

### State Persistence
- All tasks stored in memory during session
- Data lost when application exits
- No automatic save/load

### ID Management
- IDs auto-increment starting from 1
- IDs do not reuse after deletion
- ID counter persists in memory during session
