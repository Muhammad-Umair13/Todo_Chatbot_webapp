"""Unit tests for Task model.

T-007: Unit test for Task creation
Spec Ref: sp.tasks §Tests for User Story 1
"""

import pytest
from datetime import datetime

from todo_apps.models.task import Priority, Task


class TestTaskCreation:
    """Test cases for Task creation."""

    def test_task_creation_with_title_only(self):
        """Test task creation with title only."""
        task = Task(id=1, title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_creation_with_title_and_description(self):
        """Test task creation with title and description."""
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description"
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False

    def test_task_creation_with_completed_status(self):
        """Test task creation with completed status."""
        task = Task(id=1, title="Test Task", completed=True)

        assert task.completed is True

    def test_task_creation_auto_timestamps(self):
        """Test that timestamps are auto-generated."""
        before = datetime.now()
        task = Task(id=1, title="Test Task")
        after = datetime.now()

        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after


class TestTaskMethods:
    """Test cases for Task methods."""

    def test_update_title(self):
        """Test updating task title."""
        task = Task(id=1, title="Old Title")
        original_updated = task.updated_at

        # Small delay to ensure timestamp changes
        task.update_title("New Title")

        assert task.title == "New Title"
        assert task.updated_at >= original_updated

    def test_mark_complete(self):
        """Test marking task as complete."""
        task = Task(id=1, title="Test Task", completed=False)

        task.mark_complete()

        assert task.completed is True
        assert isinstance(task.updated_at, datetime)

    def test_mark_incomplete(self):
        """Test marking task as incomplete."""
        task = Task(id=1, title="Test Task", completed=True)

        task.mark_incomplete()

        assert task.completed is False
        assert isinstance(task.updated_at, datetime)
