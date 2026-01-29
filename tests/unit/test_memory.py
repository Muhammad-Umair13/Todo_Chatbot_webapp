"""Unit tests for InMemoryTaskRepository.

T-008: Unit test for MemoryAgent add
Spec Ref: sp.tasks §Tests for User Story 1
"""

import pytest

from todo_apps.models.task import Task
from todo_apps.services.memory import InMemoryTaskRepository


class TestInMemoryTaskRepository:
    """Test cases for InMemoryTaskRepository."""

    def test_save_and_get_task(self):
        """Test saving and retrieving a task."""
        repo = InMemoryTaskRepository()
        task = Task(id=1, title="Test Task")

        repo.save(task)
        retrieved = repo.get(1)

        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.title == task.title

    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist."""
        repo = InMemoryTaskRepository()

        result = repo.get(999)

        assert result is None

    def test_delete_task(self):
        """Test deleting a task."""
        repo = InMemoryTaskRepository()
        task = Task(id=1, title="Test Task")
        repo.save(task)

        repo.delete(1)

        assert repo.get(1) is None

    def test_delete_nonexistent_task(self):
        """Test deleting a task that doesn't exist."""
        repo = InMemoryTaskRepository()

        # Should not raise an error
        repo.delete(999)

    def test_list_all_empty(self):
        """Test listing all tasks when empty."""
        repo = InMemoryTaskRepository()

        tasks = repo.list_all()

        assert tasks == []

    def test_list_all_sorted_by_id(self):
        """Test that list_all returns tasks sorted by ID."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=3, title="Task 3"))
        repo.save(Task(id=1, title="Task 1"))
        repo.save(Task(id=2, title="Task 2"))

        tasks = repo.list_all()

        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_list_by_completed(self):
        """Test listing tasks by completion status."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task 1", completed=True))
        repo.save(Task(id=2, title="Task 2", completed=False))
        repo.save(Task(id=3, title="Task 3", completed=True))

        completed = repo.list_by_completed(True)
        pending = repo.list_by_completed(False)

        assert len(completed) == 2
        assert all(t.completed for t in completed)
        assert len(pending) == 1
        assert all(not t.completed for t in pending)

    def test_count(self):
        """Test counting tasks."""
        repo = InMemoryTaskRepository()
        assert repo.count() == 0

        repo.save(Task(id=1, title="Task 1"))
        assert repo.count() == 1

        repo.save(Task(id=2, title="Task 2"))
        assert repo.count() == 2

    def test_generate_id(self):
        """Test auto-incrementing ID generation."""
        repo = InMemoryTaskRepository()

        assert repo.generate_id() == 1
        assert repo.generate_id() == 2
        assert repo.generate_id() == 3

    def test_save_updates_existing_task(self):
        """Test that save updates an existing task."""
        repo = InMemoryTaskRepository()
        task = Task(id=1, title="Original Title")
        repo.save(task)

        task.title = "Updated Title"
        repo.save(task)

        retrieved = repo.get(1)
        assert retrieved.title == "Updated Title"
