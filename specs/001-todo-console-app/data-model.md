# Data Model: Todo Console Application (Phase 1)

## Task Entity

The Task is the core domain entity representing a single todo item.

### Entity Definition

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique auto-incrementing identifier for the task.
        title: Brief description of what needs to be done (1-200 chars).
        description: Detailed information about the task (max 1000 chars).
        completed: Whether the task has been finished.
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last modified.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_title(self, new_title: str) -> None:
        """Update task title and set updated_at timestamp."""
        self.title = new_title
        self.updated_at = datetime.now()

    def mark_complete(self) -> None:
        """Mark task as complete."""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark task as incomplete."""
        self.completed = False
        self.updated_at = datetime.now()
```

### Field Specifications

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | int | > 0, unique | Required | Auto-incrementing identifier |
| `title` | str | 1 <= len <= 200 | Required | Task summary |
| `description` | str | 0 <= len <= 1000 | "" | Detailed task info |
| `completed` | bool | - | False | Completion status |
| `created_at` | datetime | - | Now() | Creation timestamp |
| `updated_at` | datetime | - | Now() | Last modification |

### Validation Rules

```python
def validate_title(title: str) -> None:
    """Validate task title."""
    if not title:
        raise InvalidTitleError("Title cannot be empty")
    if len(title) > 200:
        raise InvalidTitleError("Title must be 200 characters or less")
    if not title.strip():
        raise InvalidTitleError("Title cannot be whitespace only")


def validate_description(description: str) -> None:
    """Validate task description."""
    if len(description) > 1000:
        raise InvalidDescriptionError("Description must be 1000 characters or less")
```

## Storage Model

### In-Memory Storage Structure

```python
from typing import Protocol


class TaskRepository(Protocol):
    """Protocol for task storage (enables future persistence)."""

    def save(self, task: Task) -> None: ...
    def get(self, task_id: int) -> Task | None: ...
    def delete(self, task_id: int) -> None: ...
    def list_all(self) -> list[Task]: ...
    def list_by_completed(self, completed: bool) -> list[Task]: ...
    def count(self) -> int: ...
```

### In-Memory Implementation

```python
class InMemoryTaskRepository:
    """In-memory task storage for Phase 1."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def save(self, task: Task) -> None:
        """Save or update a task."""
        self._tasks[task.id] = task

    def get(self, task_id: int) -> Task | None:
        """Retrieve a task by ID."""
        return self._tasks.get(task_id)

    def delete(self, task_id: int) -> None:
        """Delete a task by ID."""
        self._tasks.pop(task_id, None)

    def list_all(self) -> list[Task]:
        """List all tasks sorted by ID."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def list_by_completed(self, completed: bool) -> list[Task]:
        """List tasks filtered by completion status."""
        return sorted(
            (t for t in self._tasks.values() if t.completed == completed),
            key=lambda t: t.id
        )

    def count(self) -> int:
        """Return total task count."""
        return len(self._tasks)

    def generate_id(self) -> int:
        """Generate next auto-incrementing ID."""
        task_id = self._next_id
        self._next_id += 1
        return task_id
```

## Service Layer

### TaskService

```python
from dataclasses import dataclass


@dataclass
class CreateTaskInput:
    """Input for creating a task."""
    title: str
    description: str = ""


@dataclass
class UpdateTaskInput:
    """Input for updating a task."""
    title: str | None = None
    description: str | None = None


class TaskService:
    """Business logic for task operations."""

    def __init__(self, repository: InMemoryTaskRepository) -> None:
        self._repository = repository

    def create_task(self, input_data: CreateTaskInput) -> Task:
        """Create a new task."""
        validate_title(input_data.title)
        validate_description(input_data.description)

        task = Task(
            id=self._repository.generate_id(),
            title=input_data.title.strip(),
            description=input_data.description.strip()
        )
        self._repository.save(task)
        return task

    def list_tasks(self, completed_filter: bool | None = None) -> list[Task]:
        """List all tasks, optionally filtered by completion status."""
        if completed_filter is None:
            return self._repository.list_all()
        return self._repository.list_by_completed(completed_filter)

    def complete_task(self, task_id: int) -> Task:
        """Mark a task as complete."""
        task = self._get_task_or_raise(task_id)
        if task.completed:
            raise TaskAlreadyCompletedError(f"Task {task_id} is already completed")
        task.mark_complete()
        self._repository.save(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID."""
        if not self._repository.get(task_id):
            raise TaskNotFoundError(f"Task {task_id} not found")
        self._repository.delete(task_id)

    def update_task(self, task_id: int, input_data: UpdateTaskInput) -> Task:
        """Update task details."""
        task = self._get_task_or_raise(task_id)

        if input_data.title is not None:
            validate_title(input_data.title)
            task.update_title(input_data.title.strip())

        if input_data.description is not None:
            validate_description(input_data.description)
            task.description = input_data.description.strip()

        self._repository.save(task)
        return task

    def _get_task_or_raise(self, task_id: int) -> Task:
        """Get task or raise TaskNotFoundError."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task
```

## Domain Events

### Event Definitions (for future phases)

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DomainEvent:
    """Base class for domain events."""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TaskCreated(DomainEvent):
    """Event emitted when a task is created."""
    task_id: int
    title: str


@dataclass
class TaskCompleted(DomainEvent):
    """Event emitted when a task is completed."""
    task_id: int


@dataclass
class TaskDeleted(DomainEvent):
    """Event emitted when a task is deleted."""
    task_id: int
```

**Note**: Events are defined for Phase 1 but not implemented. Future phases can add event publishing.
