"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    from todo_py.models.task import Task

    return Task(id=1, title="Test Task", description="Test Description")


@pytest.fixture
def multiple_tasks():
    """Create multiple tasks for testing."""
    from todo_py.models.task import Task

    return [
        Task(id=1, title="Task 1", description="Description 1"),
        Task(id=2, title="Task 2", description="Description 2"),
        Task(id=3, title="Task 3", description="Description 3", completed=True),
    ]


@pytest.fixture
def empty_repository():
    """Create an empty in-memory task repository."""
    from todo_py.services.memory import InMemoryTaskRepository

    return InMemoryTaskRepository()


@pytest.fixture
def populated_repository(empty_repository, multiple_tasks):
    """Create a repository with multiple tasks."""
    for task in multiple_tasks:
        empty_repository.save(task)
    return empty_repository


@pytest.fixture
def task_service(populated_repository):
    """Create a TaskService with populated repository."""
    from todo_py.services.task_service import TaskService

    return TaskService(repository=populated_repository)
