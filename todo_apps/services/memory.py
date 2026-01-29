"""In-memory task storage implementation.

T-005: Implement in-memory storage in src/services/memory.py
Spec Ref: sp.specify §In-Memory Storage, sp.research.md §Data Storage Strategy
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, TypeAlias

from todo_apps.models.task import Priority, Task

TaskDict: TypeAlias = dict[int, Task]


@dataclass
class TaskFilter:
    """Filter criteria for tasks."""

    completed: bool | None = None
    priority: Priority | None = None
    tags: list[str] | None = None
    keyword: str | None = None
    due_before: datetime | None = None
    due_after: datetime | None = None


@dataclass
class TaskSort:
    """Sort criteria for tasks."""

    field: str = "created_at"  # "id", "title", "created_at", "updated_at", "due_date", "priority"
    ascending: bool = True


class TaskRepository(Protocol):
    """Protocol for task storage (enables future persistence)."""

    def save(self, task: Task) -> None: ...
    def get(self, task_id: int) -> Task | None: ...
    def delete(self, task_id: int) -> None: ...
    def list_all(self) -> list[Task]: ...
    def list_by_completed(self, completed: bool) -> list[Task]: ...
    def count(self) -> int: ...
    def generate_id(self) -> int: ...
    def search(self, filter_criteria: TaskFilter) -> list[Task]: ...
    def sort_tasks(self, tasks: list[Task], sort_criteria: TaskSort) -> list[Task]: ...


class InMemoryTaskRepository:
    """In-memory task storage for Phase 1.

    Uses a dictionary for O(1) lookup by ID.
    Auto-incrementing IDs starting from 1.
    """

    def __init__(self) -> None:
        """Initialize the in-memory task repository."""
        self._tasks: TaskDict = {}
        self._next_id: int = 1

    def save(self, task: Task) -> None:
        """Save or update a task.

        Args:
            task: The task to save.
        """
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def delete(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.
        """
        self._tasks.pop(task_id, None)

    def list_all(self) -> list[Task]:
        """List all tasks sorted by ID.

        Returns:
            List of all tasks sorted by ID.
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def list_by_completed(self, completed: bool) -> list[Task]:
        """List tasks filtered by completion status.

        Args:
            completed: Filter for completed status.

        Returns:
            List of tasks with the specified completion status, sorted by ID.
        """
        return sorted(
            (t for t in self._tasks.values() if t.completed == completed),
            key=lambda t: t.id
        )

    def count(self) -> int:
        """Return total task count.

        Returns:
            Number of tasks in storage.
        """
        return len(self._tasks)

    def generate_id(self) -> int:
        """Generate next auto-incrementing ID.

        Returns:
            The next available task ID.
        """
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def search(self, filter_criteria: TaskFilter) -> list[Task]:
        """Search tasks based on filter criteria.

        Args:
            filter_criteria: The filter criteria to apply.

        Returns:
            List of tasks matching the filter criteria.
        """
        tasks = self._tasks.values()

        # Filter by completion status
        if filter_criteria.completed is not None:
            tasks = [t for t in tasks if t.completed == filter_criteria.completed]

        # Filter by priority
        if filter_criteria.priority is not None:
            tasks = [t for t in tasks if t.priority == filter_criteria.priority]

        # Filter by tags (match any of the specified tags)
        if filter_criteria.tags:
            tasks = [
                t for t in tasks
                if any(t.has_tag(tag) for tag in filter_criteria.tags)
            ]

        # Filter by keyword in title or description
        if filter_criteria.keyword:
            tasks = [t for t in tasks if t.matches_keyword(filter_criteria.keyword)]

        # Filter by due date range
        if filter_criteria.due_before is not None:
            tasks = [
                t for t in tasks
                if t.due_date is not None and t.due_date <= filter_criteria.due_before
            ]

        if filter_criteria.due_after is not None:
            tasks = [
                t for t in tasks
                if t.due_date is not None and t.due_date >= filter_criteria.due_after
            ]

        return list(tasks)

    def sort_tasks(self, tasks: list[Task], sort_criteria: TaskSort) -> list[Task]:
        """Sort tasks based on sort criteria.

        Args:
            tasks: The list of tasks to sort.
            sort_criteria: The sort criteria to apply.

        Returns:
            Sorted list of tasks.
        """
        # Priority order mapping
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

        # Define sort key function
        def sort_key(task: Task) -> tuple:
            key_value: str | int | float | datetime | None

            if sort_criteria.field == "id":
                key_value = task.id
            elif sort_criteria.field == "title":
                key_value = task.title.lower()
            elif sort_criteria.field == "created_at":
                key_value = task.created_at
            elif sort_criteria.field == "updated_at":
                key_value = task.updated_at
            elif sort_criteria.field == "due_date":
                # Tasks with no due date go last
                key_value = task.due_date if task.due_date else datetime.max
            elif sort_criteria.field == "priority":
                key_value = priority_order.get(task.priority, 1)
            else:
                key_value = task.id  # Default to ID

            return (key_value,)

        reverse = not sort_criteria.ascending
        return sorted(tasks, key=sort_key, reverse=reverse)
