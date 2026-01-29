"""CLI command handlers.

T-011, T-016, T-021, T-026, T-031, T-036: Implement command handlers
Spec Ref: sp.contracts/cli-commands.md
"""

import sys
from datetime import datetime
from typing import Any

from todo_apps.exceptions import (
    InvalidDescriptionError,
    InvalidTitleError,
    TaskAlreadyCompletedError,
    TaskNotFoundError,
    TodoError,
)
from todo_apps.models.task import Priority, Recurrence, Task
from todo_apps.services.task_service import (
    CreateTaskInput,
    TaskService,
    UpdateTaskInput,
)
from todo_apps.utils.date_parser import parse_natural_date


def _parse_date(date_str: str) -> datetime | None:
    """Parse date string using natural language parser.

    Args:
        date_str: Date string to parse.

    Returns:
        Parsed datetime or None if empty string or invalid.
    """
    if not date_str:
        return None
    return parse_natural_date(date_str)


def _parse_tags(tags_str: str) -> list[str]:
    """Parse comma-separated tags string.

    Args:
        tags_str: Comma-separated tags.

    Returns:
        List of tags.
    """
    if not tags_str:
        return []
    return [t.lower().strip() for t in tags_str.split(",") if t.strip()]


def handle_add(args: dict[str, Any], service: TaskService) -> int:
    """Handle the 'add' command.

    Args:
        args: Parsed command arguments.
        service: TaskService instance.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        priority = Priority(args.get("priority", "medium"))
        tags = _parse_tags(args.get("tags", ""))
        due_date = _parse_date(args.get("due", ""))
        repeat_value = args.get("repeat", "") or "none"
        recurrence = Recurrence(repeat_value)

        input_data = CreateTaskInput(
            title=args["title"],
            description=args.get("description", ""),
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence,
        )
        task = service.create_task(input_data)
        details = []
        if task.tags:
            details.append(f"tags: {', '.join(task.tags)}")
        if task.due_date:
            details.append(f"due: {task.due_date.strftime('%Y-%m-%d')}")
        if task.recurrence != Recurrence.NONE:
            details.append(f"repeat: {task.recurrence.value}")

        detail_str = f" ({', '.join(details)})" if details else ""
        print(f"[+] Task created: [{task.id}] {task.title} [{task.priority.value}]{detail_str}")
        return 0
    except InvalidTitleError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except InvalidDescriptionError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1


def handle_list(args: dict[str, Any], service: TaskService) -> int:
    """Handle the 'list' command.

    Args:
        args: Parsed command arguments.
        service: TaskService instance.

    Returns:
        Exit code (0 for success).
    """
    # Parse filters
    completed_filter: bool | None = None
    if args.get("completed"):
        completed_filter = True
    elif args.get("pending"):
        completed_filter = False

    priority_filter: Priority | None = None
    if args.get("priority"):
        priority_filter = Priority(args["priority"])

    tags_filter = _parse_tags(args.get("tags", ""))
    keyword_filter = args.get("keyword", "") or None

    # Search with filters
    tasks = service.search_tasks(
        keyword=keyword_filter,
        completed=completed_filter,
        priority=priority_filter,
        tags=tags_filter if tags_filter else None,
    )

    # Sort tasks
    sort_field = args.get("sort", "created_at")
    ascending = not args.get("desc", False)
    tasks = service.sort_tasks(tasks, field=sort_field, ascending=ascending)

    if not tasks:
        print("No tasks found. Add your first task with: todo add \"Task title\"")
        return 0

    # Print header
    print("ID  | Status | Priority  | Due Date   | Title")
    print("----|--------|-----------|------------|------------------")

    # Print tasks
    for task in tasks:
        status = "x" if task.completed else " "
        priority_str = task.priority.value.center(7)
        due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else "N/A       "
        print(f"{task.id:>2} | [{status}]    | {priority_str} | {due_str} | {task.title}")
        if task.tags:
            print(f"    |        |           |            | Tags: {', '.join(task.tags)}")

    return 0


def handle_complete(args: dict[str, Any], service: TaskService) -> int:
    """Handle the 'complete' command.

    Args:
        args: Parsed command arguments.
        service: TaskService instance.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task = service.complete_task(args["task_id"])
        print(f"[+] Task [{task.id}] marked as completed")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except TaskAlreadyCompletedError as e:
        print(f"[i] Task [{e.task_id}] is already completed")
        return 0
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1


def handle_delete(args: dict[str, Any], service: TaskService) -> int:
    """Handle the 'delete' command.

    Args:
        args: Parsed command arguments.
        service: TaskService instance.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        service.delete_task(args["task_id"])
        print(f"[+] Task [{args['task_id']}] deleted")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1


def handle_update(args: dict[str, Any], service: TaskService) -> int:
    """Handle the 'update' command.

    Args:
        args: Parsed command arguments.
        service: TaskService instance.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        priority: Priority | None = None
        if args.get("priority"):
            priority = Priority(args["priority"])

        tags = _parse_tags(args.get("tags", ""))
        tags_list = tags if tags else None

        due_str = args.get("due", "")
        if due_str == "clear":
            due_date = None
        else:
            due_date = _parse_date(due_str)

        recurrence: Recurrence | None = None
        if args.get("repeat"):
            recurrence = Recurrence(args["repeat"])

        input_data = UpdateTaskInput(
            title=args["title"],
            description=args.get("description", "") or None,
            priority=priority,
            tags=tags_list,
            due_date=due_date,
            recurrence=recurrence,
        )
        task = service.update_task(args["task_id"], input_data)
        print(f"[+] Task [{task.id}] updated")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except InvalidTitleError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1


def handle_toggle(args: dict[str, Any], service: TaskService) -> int:
    """Handle the 'toggle' command.

    Args:
        args: Parsed command arguments.
        service: TaskService instance.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    try:
        task = service.toggle_task(args["task_id"])
        status = "completed" if task.completed else "incomplete"
        print(f"[+] Task [{task.id}] marked as {status}")
        return 0
    except TaskNotFoundError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
    except TodoError as e:
        print(f"Error: {e.message}", file=sys.stderr)
        return 1
