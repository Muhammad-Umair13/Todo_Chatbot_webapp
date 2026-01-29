"""CLI package - Contains command-line interface components."""

from todo_apps.cli.parser import create_parser
from todo_apps.cli.commands import handle_add, handle_list, handle_complete, handle_delete, handle_update, handle_toggle

__all__ = [
    "create_parser",
    "handle_add",
    "handle_list",
    "handle_complete",
    "handle_delete",
    "handle_update",
    "handle_toggle",
]
