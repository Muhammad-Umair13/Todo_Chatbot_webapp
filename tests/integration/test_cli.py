"""Integration tests for CLI commands.

T-009, T-014, T-019, T-024, T-029, T-034: Integration tests for all commands
Spec Ref: sp.tasks §Integration tests
"""

import subprocess
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from todo_apps.cli.parser import create_parser
from todo_apps.cli.commands import handle_add, handle_list, handle_complete, handle_delete, handle_update, handle_toggle
from todo_apps.services.memory import InMemoryTaskRepository
from todo_apps.services.task_service import CreateTaskInput, TaskService, UpdateTaskInput


class TestCLIAddCommand:
    """Integration tests for 'add' command."""

    def test_add_task_creates_task(self):
        """Test 'todo add' creates a task."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with patch("sys.argv", ["todo", "add", "Buy groceries"]):
            args = create_parser().parse_args(["add", "Buy groceries"])

        result = handle_add(vars(args), service)

        assert result == 0
        assert repo.count() == 1
        task = repo.get(1)
        assert task is not None
        assert task.title == "Buy groceries"

    def test_add_task_with_description(self):
        """Test 'todo add' with description creates task with description."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with patch("sys.argv", ["todo", "add", "Buy", "-d", "Milk, eggs, bread"]):
            args = create_parser().parse_args(["add", "Buy", "-d", "Milk, eggs, bread"])

        result = handle_add(vars(args), service)

        assert result == 0
        task = repo.get(1)
        assert task.description == "Milk, eggs, bread"

    def test_add_empty_title_shows_error(self):
        """Test 'todo add' with empty title shows error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with patch("sys.argv", ["todo", "add", ""]):
            args = create_parser().parse_args(["add", ""])

        with patch("sys.stderr", new=StringIO()) as mock_stderr:
            result = handle_add(vars(args), service)

        assert result == 1
        assert "Title cannot be empty" in mock_stderr.getvalue()


class TestCLIListCommand:
    """Integration tests for 'list' command."""

    def test_list_empty_shows_message(self, capsys):
        """Test 'todo list' with no tasks shows appropriate message."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        result = handle_list({"command": "list"}, service)

        assert result == 0
        captured = capsys.readouterr()
        assert "No tasks found" in captured.out

    def test_list_all_tasks(self, capsys):
        """Test 'todo list' shows all tasks."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Task 1"))
        service.create_task(CreateTaskInput(title="Task 2"))

        result = handle_list({"command": "list"}, service)

        assert result == 0
        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out

    def test_list_completed_filter(self, capsys):
        """Test 'todo list --completed' shows only completed."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Task 1"))
        task2 = service.create_task(CreateTaskInput(title="Task 2"))
        service.complete_task(task2.id)

        result = handle_list({"command": "list", "completed": True}, service)

        assert result == 0
        captured = capsys.readouterr()
        assert "Task 2" in captured.out
        assert "Task 1" not in captured.out


class TestCLICompleteCommand:
    """Integration tests for 'complete' command."""

    def test_complete_task(self, capsys):
        """Test 'todo complete' marks task as completed."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Task 1"))

        result = handle_complete({"command": "complete", "task_id": 1}, service)

        assert result == 0
        task = repo.get(1)
        assert task.completed is True
        captured = capsys.readouterr()
        assert "marked as completed" in captured.out

    def test_complete_nonexistent_shows_error(self, capsys):
        """Test 'todo complete' with non-existent ID shows error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        result = handle_complete({"command": "complete", "task_id": 999}, service)

        assert result == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err

    def test_complete_already_completed_shows_message(self, capsys):
        """Test 'todo complete' on already completed task shows message."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        task = service.create_task(CreateTaskInput(title="Task"))
        service.complete_task(task.id)

        result = handle_complete({"command": "complete", "task_id": 1}, service)

        assert result == 0
        captured = capsys.readouterr()
        assert "already completed" in captured.out


class TestCLIDeleteCommand:
    """Integration tests for 'delete' command."""

    def test_delete_task(self, capsys):
        """Test 'todo delete' removes task."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Task 1"))

        result = handle_delete({"command": "delete", "task_id": 1}, service)

        assert result == 0
        assert repo.get(1) is None
        captured = capsys.readouterr()
        assert "deleted" in captured.out

    def test_delete_nonexistent_shows_error(self, capsys):
        """Test 'todo delete' with non-existent ID shows error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        result = handle_delete({"command": "delete", "task_id": 999}, service)

        assert result == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err


class TestCLIUpdateCommand:
    """Integration tests for 'update' command."""

    def test_update_title(self, capsys):
        """Test 'todo update' changes title."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Old Title"))

        result = handle_update(
            {"command": "update", "task_id": 1, "title": "New Title", "description": ""},
            service
        )

        assert result == 0
        task = repo.get(1)
        assert task.title == "New Title"
        captured = capsys.readouterr()
        assert "updated" in captured.out

    def test_update_title_and_description(self, capsys):
        """Test 'todo update' with description."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Title"))

        result = handle_update(
            {"command": "update", "task_id": 1, "title": "New Title", "description": "New Desc"},
            service
        )

        assert result == 0
        task = repo.get(1)
        assert task.title == "New Title"
        assert task.description == "New Desc"

    def test_update_nonexistent_shows_error(self, capsys):
        """Test 'todo update' with non-existent ID shows error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        result = handle_update(
            {"command": "update", "task_id": 999, "title": "New", "description": ""},
            service
        )

        assert result == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err

    def test_update_empty_title_shows_error(self, capsys):
        """Test 'todo update' with empty title shows error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Title"))

        result = handle_update(
            {"command": "update", "task_id": 1, "title": "", "description": ""},
            service
        )

        assert result == 1
        captured = capsys.readouterr()
        assert "cannot be empty" in captured.err


class TestCLIToggleCommand:
    """Integration tests for 'toggle' command."""

    def test_toggle_incomplete_to_complete(self, capsys):
        """Test 'todo toggle' marks incomplete as complete."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        service.create_task(CreateTaskInput(title="Task"))

        result = handle_toggle({"command": "toggle", "task_id": 1}, service)

        assert result == 0
        task = repo.get(1)
        assert task.completed is True
        captured = capsys.readouterr()
        assert "completed" in captured.out

    def test_toggle_complete_to_incomplete(self, capsys):
        """Test 'todo toggle' marks complete as incomplete."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        task = service.create_task(CreateTaskInput(title="Task"))
        service.complete_task(task.id)

        result = handle_toggle({"command": "toggle", "task_id": 1}, service)

        assert result == 0
        task = repo.get(1)
        assert task.completed is False
        captured = capsys.readouterr()
        assert "incomplete" in captured.out

    def test_toggle_nonexistent_shows_error(self, capsys):
        """Test 'todo toggle' with non-existent ID shows error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        result = handle_toggle({"command": "toggle", "task_id": 999}, service)

        assert result == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err
