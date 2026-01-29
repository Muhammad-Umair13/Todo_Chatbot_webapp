# Research Findings: Todo Console Application (Phase 1)

## CLI Framework Evaluation

### Decision: Use Python `argparse` (stdlib)

**Rationale**:
- No external dependencies required (constitution principle IV)
- Built-in subcommand support via `argparse.ArgumentParser.add_subparsers()`
- Full Python 3.13+ type hints compatibility
- Cross-platform support (Windows, macOS, Linux)
- `--help` and `-h` flags built-in with automatic documentation
- Proven reliability in production applications

**Alternatives Considered**:

| Framework | Pros | Cons | Decision |
|-----------|------|------|----------|
| argparse (stdlib) | No deps, full features, type hints | More verbose | **Selected** |
| click | Clean decorator syntax | External dependency | Rejected |
| typer | Modern, type-safe | Requires click | Rejected |
| docopt | Beautiful docs | Non-standard parsing | Rejected |

### Implementation Pattern

```python
import argparse

parser = argparse.ArgumentParser(prog="todo", description="Manage tasks")
subparsers = parser.add_subparsers(dest="command", required=True)

# Add subcommand
add_parser = subparsers.add_parser("add", help="Add a new task")
add_parser.add_argument("title", help="Task title")
add_parser.add_argument("-d", "--description", help="Task description")
```

## Data Storage Strategy

### Decision: Dictionary-based in-memory storage

**Rationale**:
- O(1) lookup complexity for all operations
- Simple ID-based task retrieval
- Auto-incrementing ID generation is trivial
- Memory-efficient for single-session use
- Easy migration path to database (Phase 2+)

**Storage Structure**:

```python
tasks: dict[int, Task] = {}
next_id: int = 1
```

### Operations Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Add task | O(1) | Append to dict |
| Get task | O(1) | Direct ID lookup |
| List tasks | O(n) | Iterate all values |
| Update task | O(1) | Direct ID lookup + dict update |
| Delete task | O(1) | Direct ID lookup + dict delete |
| Filter tasks | O(n) | Filter all values |

## Task ID Management

### Decision: Counter-based auto-increment

**Rationale**:
- Simple integer sequence (1, 2, 3, ...)
- Predictable, user-friendly IDs
- No ID reuse after deletion (avoids confusion)
- Easy serialization for future phases

**Implementation**:

```python
class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate next available task ID."""
        task_id = self._next_id
        self._next_id += 1
        return task_id
```

## Python 3.13+ Best Practices

### Type Hints

All function signatures MUST include type hints:

```python
def add_task(self, title: str, description: str = "") -> Task:
    """Add a new task with title and optional description."""
    ...
```

### Dataclasses

Use `@dataclass` for the Task model:

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

### Docstring Format

Use Google-style docstrings:

```python
def complete_task(self, task_id: int) -> Task:
    """Mark a task as completed.

    Args:
        task_id: The unique identifier of the task to complete.

    Returns:
        The updated Task object.

    Raises:
        TaskNotFoundError: If task with given ID doesn't exist.
        TaskAlreadyCompletedError: If task is already completed.
    """
    ...
```

## Error Handling Strategy

### Custom Exceptions

```python
class TodoError(Exception):
    """Base exception for todo application errors."""

class TaskNotFoundError(TodoError):
    """Raised when a task ID is not found."""

class InvalidTitleError(TodoError):
    """Raised when task title is invalid."""

class TaskAlreadyCompletedError(TodoError):
    """Raised when attempting to complete an already completed task."""
```

### User-Friendly Messages

All errors should be displayed to stderr with clear, actionable messages:

```python
try:
    task = service.complete_task(task_id)
except TaskNotFoundError:
    print(f"Error: Task {task_id} not found.", file=sys.stderr)
    sys.exit(1)
```

## Testing Strategy

### Test Framework: pytest

**Rationale**:
- Industry standard for Python
- Fixture support for test setup
- Parameterized tests for multiple scenarios
- Coverage reporting with pytest-cov

### Test Structure

```
tests/
├── conftest.py           # Shared fixtures
├── unit/
│   ├── test_task.py      # Task model tests
│   ├── test_service.py   # Service layer tests
│   └── test_cli.py       # CLI parser tests
└── integration/
    └── test_cli.py       # End-to-end CLI tests
```

### Coverage Requirements

- 100% coverage for new code
- All edge cases covered
- Negative test cases included

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |

## Future Phase Considerations

### Phase 2: Persistence

The in-memory storage should be abstracted behind an interface:

```python
class TaskRepository(Protocol):
    """Abstract storage interface for future persistence."""

    def save(self, task: Task) -> None: ...
    def get(self, task_id: int) -> Task | None: ...
    def delete(self, task_id: int) -> None: ...
    def list_all(self) -> list[Task]: ...
```

### Phase 3: Web API

The service layer can be reused for a web API:

```python
# Reuse TaskService for web endpoints
@app.post("/tasks")
def create_task(request: CreateTaskRequest) -> Task:
    return service.add_task(request.title, request.description)
```

### Phase 5: Cloud Deployment

Containerize the application:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["todo", "--help"]
```
