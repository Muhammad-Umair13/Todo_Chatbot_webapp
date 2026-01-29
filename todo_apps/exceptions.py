"""Custom exceptions for the Todo application.

T-006: Create custom exceptions in src/exceptions.py
Spec Ref: sp.research.md §Error Handling Strategy
"""


class TodoError(Exception):
    """Base exception for todo application errors."""

    def __init__(self, message: str) -> None:
        """Initialize TodoError with a message."""
        self.message = message
        super().__init__(message)


class TaskNotFoundError(TodoError):
    """Raised when a task ID is not found."""

    def __init__(self, task_id: int) -> None:
        """Initialize TaskNotFoundError with task ID."""
        message = f"Task {task_id} not found."
        super().__init__(message)
        self.task_id = task_id


class InvalidTitleError(TodoError):
    """Raised when task title is invalid."""

    def __init__(self, message: str = "Title is invalid.") -> None:
        """Initialize InvalidTitleError with message."""
        super().__init__(message)


class InvalidDescriptionError(TodoError):
    """Raised when task description is invalid."""

    def __init__(self, message: str = "Description is invalid.") -> None:
        """Initialize InvalidDescriptionError with message."""
        super().__init__(message)


class TaskAlreadyCompletedError(TodoError):
    """Raised when attempting to complete an already completed task."""

    def __init__(self, task_id: int) -> None:
        """Initialize TaskAlreadyCompletedError with task ID."""
        message = f"Task {task_id} is already completed."
        super().__init__(message)
        self.task_id = task_id
