"""CLI argument parser using argparse.

T-012, T-017, T-022, T-027, T-032, T-037: Register subparsers for all commands
Spec Ref: sp.contracts/cli-commands.md
"""

import argparse
import sys
from datetime import datetime
from typing import Any


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the todo application.

    Returns:
        Configured ArgumentParser.
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Manage your todo list",
        exit_on_error=False,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands",
        required=True,
    )

    # Register subcommands
    _add_add_subparser(subparsers)
    _add_list_subparser(subparsers)
    _add_complete_subparser(subparsers)
    _add_delete_subparser(subparsers)
    _add_update_subparser(subparsers)
    _add_toggle_subparser(subparsers)

    return parser


def _add_add_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Add 'add' subcommand to parser.

    Args:
        subparsers: The subparsers action to add to.
    """
    add_parser = subparsers.add_parser(
        "add",
        help="Add a new task",
        description="Create a new task with a title and optional details.",
    )
    add_parser.add_argument(
        "title",
        help="Task title (1-200 characters)",
    )
    add_parser.add_argument(
        "-d",
        "--description",
        help="Task description (max 1000 characters)",
        default="",
    )
    add_parser.add_argument(
        "-p",
        "--priority",
        choices=["high", "medium", "low"],
        default="medium",
        help="Task priority (default: medium)",
    )
    add_parser.add_argument(
        "-t",
        "--tags",
        help="Comma-separated tags (e.g., work,personal)",
        default="",
    )
    add_parser.add_argument(
        "--due",
        help="Due date (YYYY-MM-DD or natural language like 'tomorrow', 'next monday')",
        default="",
    )
    add_parser.add_argument(
        "-r",
        "--repeat",
        choices=["daily", "weekly", "monthly"],
        help="Repeat pattern (daily, weekly, monthly)",
        default="",
    )


def _add_list_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Add 'list' subcommand to parser.

    Args:
        subparsers: The subparsers action to add to.
    """
    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks",
        description="Display all tasks or filter by various criteria.",
    )
    list_parser.add_argument(
        "--completed",
        action="store_true",
        help="Show only completed tasks",
    )
    list_parser.add_argument(
        "--pending",
        action="store_true",
        help="Show only incomplete tasks",
    )
    list_parser.add_argument(
        "-p",
        "--priority",
        choices=["high", "medium", "low"],
        help="Filter by priority",
    )
    list_parser.add_argument(
        "-t",
        "--tags",
        help="Filter by tags (comma-separated)",
        default="",
    )
    list_parser.add_argument(
        "--keyword",
        help="Search by keyword in title/description",
        default="",
    )
    list_parser.add_argument(
        "--sort",
        choices=["id", "title", "created_at", "updated_at", "due_date", "priority"],
        default="created_at",
        help="Sort by field (default: created_at)",
    )
    list_parser.add_argument(
        "--asc",
        action="store_true",
        help="Sort in ascending order (default)",
    )
    list_parser.add_argument(
        "--desc",
        action="store_true",
        help="Sort in descending order",
    )


def _add_complete_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Add 'complete' subcommand to parser.

    Args:
        subparsers: The subparsers action to add to.
    """
    complete_parser = subparsers.add_parser(
        "complete",
        help="Mark a task as complete",
        description="Mark a task as completed by its ID.",
    )
    complete_parser.add_argument(
        "task_id",
        type=int,
        help="Task ID to complete",
    )


def _add_delete_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Add 'delete' subcommand to parser.

    Args:
        subparsers: The subparsers action to add to.
    """
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task",
        description="Delete a task by its ID.",
    )
    delete_parser.add_argument(
        "task_id",
        type=int,
        help="Task ID to delete",
    )


def _add_update_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Add 'update' subcommand to parser.

    Args:
        subparsers: The subparsers action to add to.
    """
    update_parser = subparsers.add_parser(
        "update",
        help="Update a task",
        description="Update a task's details.",
    )
    update_parser.add_argument(
        "task_id",
        type=int,
        help="Task ID to update",
    )
    update_parser.add_argument(
        "title",
        help="New task title (1-200 characters)",
    )
    update_parser.add_argument(
        "-d",
        "--description",
        help="New task description (max 1000 characters)",
        default="",
    )
    update_parser.add_argument(
        "-p",
        "--priority",
        choices=["high", "medium", "low"],
        help="Update task priority",
    )
    update_parser.add_argument(
        "-t",
        "--tags",
        help="Update tags (comma-separated)",
        default="",
    )
    update_parser.add_argument(
        "--due",
        help="Update due date (YYYY-MM-DD, NL, or 'clear')",
        default="",
    )
    update_parser.add_argument(
        "-r",
        "--repeat",
        choices=["daily", "weekly", "monthly", "none"],
        help="Update repeat pattern",
    )


def _add_toggle_subparser(subparsers: argparse._SubParsersAction) -> None:
    """Add 'toggle' subcommand to parser.

    Args:
        subparsers: The subparsers action to add to.
    """
    toggle_parser = subparsers.add_parser(
        "toggle",
        help="Toggle task completion status",
        description="Toggle a task between complete and incomplete.",
    )
    toggle_parser.add_argument(
        "task_id",
        type=int,
        help="Task ID to toggle",
    )


def parse_args(args: list[str] | None = None) -> dict[str, Any]:
    """Parse command line arguments.

    Args:
        args: Arguments to parse. Defaults to sys.argv[1:].

    Returns:
        Dictionary of parsed arguments.
    """
    parser = create_parser()
    parsed = parser.parse_args(args)

    return vars(parsed)


def main() -> int:
    """Main entry point for CLI parsing.

    Returns:
        Exit code.
    """
    try:
        args = parse_args()
        print(f"Command: {args['command']}")
        return 0
    except SystemExit:
        return 0
