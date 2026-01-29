"""Task business logic implementation.

T-010, T-015, T-020, T-025, T-030, T-035: Implement TaskService methods
Spec Ref: sp.specify §Functional Requirements, sp.data-model.md §Service Layer
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from todo_apps.exceptions import (
    InvalidDescriptionError,
    InvalidTitleError,
    TaskAlreadyCompletedError,
    TaskNotFoundError,
)
from todo_apps.models.task import Priority, Recurrence, Task
from todo_apps.services.memory import (
    InMemoryTaskRepository,
    TaskFilter,
    TaskRepository,
    TaskSort,
)


@dataclass
class CreateTaskInput:
    """Input for creating a task."""
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    tags: list[str] | None = None
    due_date: datetime | None = None
    recurrence: Recurrence = Recurrence.NONE


@dataclass
class UpdateTaskInput:
    """Input for updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Priority | None = None
    tags: list[str] | None = None
    due_date: datetime | None = None
    recurrence: Recurrence | None = None


def validate_title(title: str) -> None:
    """Validate task title.

    Args:
        title: The title to validate.

    Raises:
        InvalidTitleError: If title is empty or too long.
    """
    if not title:
        raise InvalidTitleError("Title cannot be empty.")
    if len(title) > 200:
        raise InvalidTitleError("Title must be 200 characters or less.")
    if not title.strip():
        raise InvalidTitleError("Title cannot be whitespace only.")


def validate_description(description: str) -> None:
    """Validate task description.

    Args:
        description: The description to validate.

    Raises:
        InvalidDescriptionError: If description is too long.
    """
    if len(description) > 1000:
        raise InvalidDescriptionError("Description must be 1000 characters or less.")


class TaskService:
    """Business logic for task operations."""

    def __init__(self, repository: TaskRepository | None = None) -> None:
        """Initialize TaskService with optional repository.

        Args:
            repository: Optional TaskRepository. Creates InMemoryTaskRepository if None.
        """
        self._repository = repository or InMemoryTaskRepository()

    def create_task(self, input_data: CreateTaskInput) -> Task:
        """Create a new task.

        Args:
            input_data: The task creation input.

        Returns:
            The created task.

        Raises:
            InvalidTitleError: If title is invalid.
            InvalidDescriptionError: If description is invalid.
        """
        validate_title(input_data.title)
        validate_description(input_data.description)

        task = Task(
            id=self._repository.generate_id(),
            title=input_data.title.strip(),
            description=input_data.description.strip(),
            priority=input_data.priority,
            recurrence=input_data.recurrence,
        )

        if input_data.tags:
            task.set_tags(input_data.tags)

        if input_data.due_date:
            task.set_due_date(input_data.due_date)

        self._repository.save(task)
        return task

    def list_tasks(self, completed_filter: Optional[bool] = None) -> list[Task]:
        """List all tasks, optionally filtered by completion status.

        Args:
            completed_filter: Filter for completion status. None means all tasks.

        Returns:
            List of tasks matching the filter.
        """
        if completed_filter is None:
            return self._repository.list_all()
        return self._repository.list_by_completed(completed_filter)

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to complete.

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If task does not exist.
            TaskAlreadyCompletedError: If task is already completed.
        """
        task = self._get_task_or_raise(task_id)
        if task.completed:
            raise TaskAlreadyCompletedError(task_id)

        task.mark_complete()
        self._repository.save(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Raises:
            TaskNotFoundError: If task does not exist.
        """
        if not self._repository.get(task_id):
            raise TaskNotFoundError(task_id)
        self._repository.delete(task_id)

    def update_task(self, task_id: int, input_data: UpdateTaskInput) -> Task:
        """Update task details.

        Args:
            task_id: The ID of the task to update.
            input_data: The update input.

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If task does not exist.
            InvalidTitleError: If title is provided and invalid.
        """
        task = self._get_task_or_raise(task_id)

        if input_data.title is not None:
            validate_title(input_data.title)
            task.update_title(input_data.title.strip())

        if input_data.description is not None:
            validate_description(input_data.description)
            task.description = input_data.description.strip()

        if input_data.priority is not None:
            task.set_priority(input_data.priority)

        if input_data.tags is not None:
            task.set_tags(input_data.tags)

        if input_data.due_date is not None:
            task.set_due_date(input_data.due_date)

        if input_data.recurrence is not None:
            task.set_recurrence(input_data.recurrence)

        self._repository.save(task)
        return task

    def search_tasks(
        self,
        keyword: str | None = None,
        completed: bool | None = None,
        priority: Priority | None = None,
        tags: list[str] | None = None,
        due_before: datetime | None = None,
        due_after: datetime | None = None,
    ) -> list[Task]:
        """Search tasks with multiple filter criteria.

        Args:
            keyword: Search in title and description.
            completed: Filter by completion status.
            priority: Filter by priority.
            tags: Filter by tags (matches any).
            due_before: Filter tasks due before this date.
            due_after: Filter tasks due after this date.

        Returns:
            List of matching tasks.
        """
        filter_criteria = TaskFilter(
            completed=completed,
            priority=priority,
            tags=tags,
            keyword=keyword,
            due_before=due_before,
            due_after=due_after,
        )
        return self._repository.search(filter_criteria)

    def sort_tasks(
        self,
        tasks: list[Task],
        field: str = "created_at",
        ascending: bool = True,
    ) -> list[Task]:
        """Sort tasks by specified field.

        Args:
            tasks: List of tasks to sort.
            field: Field to sort by (id, title, created_at, updated_at, due_date, priority).
            ascending: Sort order.

        Returns:
            Sorted list of tasks.
        """
        sort_criteria = TaskSort(field=field, ascending=ascending)
        return self._repository.sort_tasks(tasks, sort_criteria)

    def toggle_task(self, task_id: int) -> Task:
        """Toggle task completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If task does not exist.
        """
        task = self._get_task_or_raise(task_id)
        if task.completed:
            task.mark_incomplete()
        else:
            task.mark_complete()
        self._repository.save(task)
        return task

    def _get_task_or_raise(self, task_id: int) -> Task:
        """Get task or raise TaskNotFoundError.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task.

        Raises:
            TaskNotFoundError: If task does not exist.
        """
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    @property
    def repository(self) -> TaskRepository:
        """Get the task repository."""
        return self._repository
