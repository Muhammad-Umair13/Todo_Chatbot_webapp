"""Main entry point for the todo application.

T-038: Implement main entry point in src/main.py
Spec Ref: sp.plan §Architecture Overview
"""

import sys
from typing import Any

from todo_apps.cli.commands import (
    handle_add,
    handle_complete,
    handle_delete,
    handle_list,
    handle_toggle,
    handle_update,
)
from todo_apps.cli.menu import run_interactive_menu
from todo_apps.cli.parser import create_parser, parse_args
from todo_apps.services.memory import InMemoryTaskRepository
from todo_apps.services.task_service import TaskService


def main() -> int:
    """Main entry point for the todo application.

    Returns:
        Exit code (0 for success, non-zero for error).
    """
    # Initialize service with in-memory storage
    repository = InMemoryTaskRepository()
    service = TaskService(repository=repository)

    # Interactive mode if no arguments or specifically requested
    if len(sys.argv) == 1 or "--interactive" in sys.argv:
        if "--interactive" in sys.argv:
            sys.argv.remove("--interactive")
        return run_interactive_menu(service)

    # CLI mode with argparse (Quick Commands)
    try:
        args = parse_args()
    except SystemExit:
        return 0
    except Exception as e:
        # Default to interactive if parsing fails and it wasn't a help call
        if "-h" not in sys.argv and "--help" not in sys.argv:
            return run_interactive_menu(service)
        print(f"Error: {e}", file=sys.stderr)
        return 1

    command = args.get("command")

    # Route to appropriate handler
    handlers: dict[str, Any] = {
        "add": handle_add,
        "list": handle_list,
        "complete": handle_complete,
        "delete": handle_delete,
        "update": handle_update,
        "toggle": handle_toggle,
    }

    handler = handlers.get(command)
    if handler:
        return handler(args, service)

    print(f"Error: Unknown command: {command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
