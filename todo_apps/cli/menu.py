"""Interactive menu for the todo application."""

import sys
from datetime import datetime
from typing import Any, Callable

from todo_apps.exceptions import (
    InvalidDescriptionError,
    InvalidTitleError,
    TaskAlreadyCompletedError,
    TaskNotFoundError,
)
from todo_apps.models.task import Priority, Recurrence, Task
from todo_apps.services.task_service import (
    CreateTaskInput,
    TaskService,
    UpdateTaskInput,
)
from todo_apps.utils.date_parser import parse_natural_date


class Colors:
    """ANSI color codes for the CLI."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class InteractiveCLI:
    """Handles the interactive menu interface for the todo application."""

    def __init__(self, service: TaskService) -> None:
        """Initialize with TaskService.

        Args:
            service: TaskService instance.
        """
        self.service = service

    def clear_screen(self) -> None:
        """Clear the console screen."""
        print("\033[H\033[J", end="")

    def show_header(self, title: str) -> None:
        """Show a styled header.

        Args:
            title: Title to display in the header.
        """
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 40}")
        print(f" {title.center(38)}")
        print(f"{'=' * 40}{Colors.END}\n")

    def show_menu(self, title: str, options: list[str]) -> int | None:
        """Display a menu and get user choice.

        Args:
            title: Menu title.
            options: List of menu options.

        Returns:
            The selected option index (1-based), or None for exit.
        """
        self.show_header(title)
        for i, option in enumerate(options, 1):
            print(f" {Colors.CYAN}{i}.{Colors.END} {option}")
        print(f" {Colors.CYAN}Q.{Colors.END} Exit/Back")

        while True:
            choice = input(f"\nChoose an option (1-{len(options)}): ").strip().lower()
            if choice in ("q", "quit", "exit", "b", "back"):
                return None
            try:
                idx = int(choice)
                if 1 <= idx <= len(options):
                    return idx
                print(f"{Colors.RED}[!] Please choose between 1 and {len(options)}{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}[!] Invalid input. Enter a number or Q to exit.{Colors.END}")

    def prompt_text(self, message: str, default: str = "", required: bool = False) -> str:
        """Prompt for text input.

        Args:
            message: Message to display.
            default: Default value if input is empty.
            required: Whether input is required.

        Returns:
            The user's input.
        """
        suffix = f" (default: {default})" if default else ""
        if required:
            suffix = f" {Colors.YELLOW}(required){Colors.END}"

        while True:
            val = input(f"{message}{suffix}: ").strip()
            if not val:
                if required:
                    print(f"{Colors.RED}[!] This field is required.{Colors.END}")
                    continue
                return default
            return val

    def prompt_confirm(self, message: str, default: bool = True) -> bool:
        """Prompt for confirmation (y/n).

        Args:
            message: Message to display.
            default: Default value if input is empty.

        Returns:
            True for yes, False for no.
        """
        suffix = " (Y/n)" if default else " (y/N)"
        val = input(f"{message}{suffix}: ").strip().lower()
        if not val:
            return default
        return val.startswith("y")

    def prompt_choice(self, message: str, choices: list[tuple[str, str]]) -> str:
        """Prompt for a choice from a list.

        Args:
            message: Message to display.
            choices: List of (label, value) tuples.

        Returns:
            The selected value.
        """
        print(f"\n{message}:")
        for i, (label, _) in enumerate(choices, 1):
            print(f" {Colors.CYAN}{i}.{Colors.END} {label}")

        while True:
            choice = input(f"Choose (1-{len(choices)}): ").strip()
            try:
                idx = int(choice)
                if 1 <= idx <= len(choices):
                    return choices[idx - 1][1]
                print(f"{Colors.RED}[!] Choose between 1 and {len(choices)}{Colors.END}")
            except ValueError:
                print(f"{Colors.RED}[!] Enter a number corresponding to your choice.{Colors.END}")

    def get_priority_visual(self, priority: Priority) -> str:
        """Get visual indicator for priority.

        Args:
            priority: The priority level.

        Returns:
            Visual string with emoji and color.
        """
        if priority == Priority.HIGH:
            return f"{Colors.RED}🔴 High{Colors.END}"
        if priority == Priority.MEDIUM:
            return f"{Colors.YELLOW}🟡 Medium{Colors.END}"
        if priority == Priority.LOW:
            return f"{Colors.GREEN}🟢 Low{Colors.END}"
        return "⚪ None"

    def get_status_visual(self, task: Task) -> str:
        """Get visual indicator for task status.

        Args:
            task: The task.

        Returns:
            Status icon string.
        """
        if task.completed:
            return f"{Colors.GREEN}[✓]{Colors.END}"
        # Could add logic for overdue, etc. later
        return "[ ]"

    def run_main_menu(self) -> int:
        """Run the main menu loop.

        Returns:
            Exit code.
        """
        options = [
            "Add New Task",
            "View/List Tasks",
            "Mark Task Complete",
            "Update Task",
            "Delete Task",
            "Advanced Features",
        ]

        while True:
            self.clear_screen()
            choice = self.show_menu("MAIN MENU", options)

            if choice is None:
                print(f"\n{Colors.BLUE}Goodbye!{Colors.END}")
                return 0

            # Map choice to handler methods
            handlers = {
                1: self.run_add_task_wizard,
                2: self.run_view_tasks_menu,
                3: self.run_complete_task,
                4: self.run_update_task_wizard,
                5: self.run_delete_task,
                6: self.run_advanced_menu,
            }

            handler = handlers.get(choice)
            if handler:
                handler()
                input(f"\n{Colors.BLUE}Press Enter to return to menu...{Colors.END}")

    def run_add_task_wizard(self) -> None:
        """Interactive wizard to add a new task."""
        self.show_header("ADD TASK")

        try:
            title = self.prompt_text("Enter task title", required=True)
            description = ""
            if self.prompt_confirm("Add description?"):
                description = self.prompt_text("Enter description")

            priority = Priority.MEDIUM
            if self.prompt_confirm("Set priority?"):
                priority = Priority(self.prompt_choice("Choose priority", [
                    (self.get_priority_visual(Priority.HIGH), Priority.HIGH.value),
                    (self.get_priority_visual(Priority.MEDIUM), Priority.MEDIUM.value),
                    (self.get_priority_visual(Priority.LOW), Priority.LOW.value),
                ]))

            tags = []
            if self.prompt_confirm("Add tags?"):
                tags_str = self.prompt_text("Enter tags (comma separated)")
                if tags_str:
                    tags = [t.lower().strip() for t in tags_str.split(",") if t.strip()]

            due_date = None
            if self.prompt_confirm("Set due date?"):
                due_str = self.prompt_text("Enter due date (e.g. tomorrow, 2025-12-31)")
                due_date = parse_natural_date(due_str)
                if not due_date and due_str:
                    print(f"{Colors.YELLOW}[!] Could not parse date. Setting to None.{Colors.END}")

            recurrence = Recurrence.NONE
            if self.prompt_confirm("Make recurring?"):
                recurrence = Recurrence(self.prompt_choice("Choose frequency", [
                    ("Daily", Recurrence.DAILY.value),
                    ("Weekly", Recurrence.WEEKLY.value),
                    ("Monthly", Recurrence.MONTHLY.value),
                ]))

            input_data = CreateTaskInput(
                title=title,
                description=description,
                priority=priority,
                tags=tags,
                due_date=due_date,
                recurrence=recurrence,
            )
            task = self.service.create_task(input_data)
            print(f"\n{Colors.GREEN}✓ Task added: \"{task.title}\" (ID: {task.id}){Colors.END}")
            print(f"Priority: {self.get_priority_visual(task.priority)} | Tags: {', '.join(task.tags) or 'None'}")
            if task.due_date:
                print(f"Due: {task.due_date.strftime('%Y-%m-%d')} | Repeats: {task.recurrence.value}")

        except (InvalidTitleError, InvalidDescriptionError) as e:
            print(f"{Colors.RED}[!] Error: {e.message}{Colors.END}")

    def run_view_tasks_menu(self) -> None:
        """Menu for listing and filtering tasks."""
        options = [
            "All Tasks",
            "Pending Only",
            "Completed Only",
            "Filter by Priority",
            "Search by Keyword",
            "Filter by Tag",
        ]

        choice = self.show_menu("VIEW TASKS", options)
        if choice is None:
            return

        completed = None
        priority = None
        keyword = None
        tags = None

        if choice == 2: completed = False
        elif choice == 3: completed = True
        elif choice == 4:
            priority = Priority(self.prompt_choice("Select Priority", [
                (self.get_priority_visual(Priority.HIGH), Priority.HIGH.value),
                (self.get_priority_visual(Priority.MEDIUM), Priority.MEDIUM.value),
                (self.get_priority_visual(Priority.LOW), Priority.LOW.value),
            ]))
        elif choice == 5:
            keyword = self.prompt_text("Enter keyword to search")
        elif choice == 6:
            tag_input = self.prompt_text("Enter tag to filter by")
            if tag_input:
                tags = [t.lower().strip() for t in tag_input.split(",") if t.strip()]

        tasks = self.service.search_tasks(
            completed=completed,
            priority=priority,
            keyword=keyword,
            tags=tags
        )

        if not tasks:
            print(f"{Colors.YELLOW}No tasks found matching your filters.{Colors.END}")
            return

        # Sort by ID ascending (1, 2, 3...)
        tasks = self.service.sort_tasks(tasks, field="id", ascending=True)

        self.display_task_list(tasks)

    def display_task_list(self, tasks: list[Task]) -> None:
        """Display a list of tasks in a detailed view."""
        print(f"\n{Colors.BOLD}{'ID':<4} | {'Status':<6} | {'Priority':<15} | {'Due Date':<10} | {'Title'}{Colors.END}")
        print("-" * 70)
        for task in tasks:
            status = self.get_status_visual(task)
            priority = self.get_priority_visual(task.priority)
            due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "N/A"
            print(f"{task.id:<4} | {status:<15} | {priority:<24} | {due:<10} | {task.title}")
            if task.tags:
                print(f"     | Tags: {Colors.CYAN}{', '.join(task.tags)}{Colors.END}")

    def run_complete_task(self) -> None:
        """Interactive complete task."""
        self.show_header("MARK COMPLETE")
        task_id_str = self.prompt_text("Enter task ID to complete", required=True)
        try:
            task_id = int(task_id_str)
            task = self.service.complete_task(task_id)
            print(f"{Colors.GREEN}✓ Task [{task.id}] marked as completed.{Colors.END}")
        except TaskAlreadyCompletedError as e:
            print(f"{Colors.YELLOW}[!] {str(e)}{Colors.END}")
        except (ValueError, TaskNotFoundError) as e:
            print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")

    def run_update_task_wizard(self) -> None:
        """Interactive update task wizard."""
        self.show_header("UPDATE TASK")
        task_id_str = self.prompt_text("Enter task ID to update", required=True)
        try:
            task_id = int(task_id_str)
            task = self.service._repository.get(task_id)
            if not task:
                raise TaskNotFoundError(task_id)

            print(f"\nUpdating: {task.title}")
            title = self.prompt_text(f"New title", default=task.title)
            desc = self.prompt_text(f"New description", default=task.description)

            priority = None
            if self.prompt_confirm("Change priority?"):
                priority = Priority(self.prompt_choice("Choose priority", [
                    (self.get_priority_visual(Priority.HIGH), Priority.HIGH.value),
                    (self.get_priority_visual(Priority.MEDIUM), Priority.MEDIUM.value),
                    (self.get_priority_visual(Priority.LOW), Priority.LOW.value),
                ]))

            input_data = UpdateTaskInput(title=title, description=desc, priority=priority)
            self.service.update_task(task_id, input_data)
            print(f"{Colors.GREEN}✓ Task [{task_id}] updated successfully.{Colors.END}")
        except (ValueError, TaskNotFoundError) as e:
            print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")

    def run_delete_task(self) -> None:
        """Interactive delete task."""
        self.show_header("DELETE TASK")
        task_id_str = self.prompt_text("Enter task ID to delete", required=True)
        try:
            task_id = int(task_id_str)
            if self.prompt_confirm(f"Are you sure you want to delete task {task_id}?", default=False):
                self.service.delete_task(task_id)
                print(f"{Colors.GREEN}✓ Task [{task_id}] deleted.{Colors.END}")
            else:
                print("Operation cancelled.")
        except (ValueError, TaskNotFoundError) as e:
            print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")

    def run_advanced_menu(self) -> None:
        """Advanced features menu."""
        options = [
            "Recurring Tasks Management",
            "Statistics & Reports",
        ]
        choice = self.show_menu("ADVANCED FEATURES", options)
        if choice == 1:
            self.run_recurring_tasks_management()
        elif choice == 2:
            self.run_statistics()

    def run_recurring_tasks_management(self) -> None:
        """Manage recurring tasks."""
        self.show_header("RECURRING TASKS")
        tasks = self.service.search_tasks()
        recurring = [t for t in tasks if t.recurrence != Recurrence.NONE]

        if not recurring:
            print(f"{Colors.YELLOW}No recurring tasks found.{Colors.END}")
            return

        for t in recurring:
            print(f"[{t.id}] {t.title} - {t.recurrence.value}")

    def run_statistics(self) -> None:
        """Show simple statistics."""
        self.show_header("STATISTICS")
        tasks = self.service.search_tasks()
        total = len(tasks)
        completed = len([t for t in tasks if t.completed])
        pending = total - completed

        print(f"Total Tasks: {total}")
        print(f"Completed: {Colors.GREEN}{completed}{Colors.END}")
        print(f"Pending: {Colors.YELLOW}{pending}{Colors.END}")

        if total > 0:
            print(f"Completion Rate: {(completed/total)*100:.1f}%")


def run_interactive_menu(service: TaskService) -> int:
    """Run the interactive menu loop.

    Args:
        service: TaskService instance.

    Returns:
        Exit code (0 for success).
    """
    cli = InteractiveCLI(service)
    return cli.run_main_menu()
