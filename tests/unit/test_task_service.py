"""Unit tests for TaskService.

T-013, T-018, T-023, T-028, T-033: Unit tests for all service methods
Spec Ref: sp.tasks §Tests for User Stories 1-6
"""

import pytest

from todo_apps.exceptions import (
    InvalidDescriptionError,
    InvalidTitleError,
    TaskAlreadyCompletedError,
    TaskNotFoundError,
)
from todo_apps.models.task import Priority, Task
from todo_apps.services.memory import InMemoryTaskRepository
from todo_apps.services.task_service import (
    CreateTaskInput,
    TaskService,
    UpdateTaskInput,
    validate_description,
    validate_title,
)


class TestValidateTitle:
    """Test cases for title validation."""

    def test_valid_title(self):
        """Test valid title passes validation."""
        validate_title("Valid Title")

    def test_empty_title_raises_error(self):
        """Test empty title raises InvalidTitleError."""
        with pytest.raises(InvalidTitleError) as exc_info:
            validate_title("")
        assert "cannot be empty" in str(exc_info.value.message)

    def test_whitespace_only_title_raises_error(self):
        """Test whitespace-only title raises InvalidTitleError."""
        with pytest.raises(InvalidTitleError) as exc_info:
            validate_title("   ")
        assert "cannot be whitespace only" in str(exc_info.value.message)

    def test_title_too_long_raises_error(self):
        """Test title over 200 chars raises InvalidTitleError."""
        with pytest.raises(InvalidTitleError) as exc_info:
            validate_title("x" * 201)
        assert "200 characters or less" in str(exc_info.value.message)

    def test_title_at_max_length_is_valid(self):
        """Test title at exactly 200 chars is valid."""
        validate_title("x" * 200)


class TestValidateDescription:
    """Test cases for description validation."""

    def test_valid_description(self):
        """Test valid description passes validation."""
        validate_description("Valid description")

    def test_empty_description_is_valid(self):
        """Test empty description is valid."""
        validate_description("")

    def test_description_too_long_raises_error(self):
        """Test description over 1000 chars raises error."""
        with pytest.raises(InvalidDescriptionError) as exc_info:
            validate_description("x" * 1001)
        assert "1000 characters or less" in str(exc_info.value.message)

    def test_description_at_max_length_is_valid(self):
        """Test description at exactly 1000 chars is valid."""
        validate_description("x" * 1000)


class TestTaskServiceCreate:
    """Test cases for TaskService.create_task."""

    def test_create_task_with_title_only(self):
        """Test creating a task with title only."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        input_data = CreateTaskInput(title="Test Task")

        task = service.create_task(input_data)

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_with_description(self):
        """Test creating a task with description."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        input_data = CreateTaskInput(title="Test", description="Description")

        task = service.create_task(input_data)

        assert task.description == "Description"

    def test_create_task_auto_increments_id(self):
        """Test that task IDs are auto-incremented."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        task1 = service.create_task(CreateTaskInput(title="Task 1"))
        task2 = service.create_task(CreateTaskInput(title="Task 2"))
        task3 = service.create_task(CreateTaskInput(title="Task 3"))

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_strips_whitespace(self):
        """Test that whitespace is stripped from inputs."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)
        input_data = CreateTaskInput(title="  Title  ", description="  Desc  ")

        task = service.create_task(input_data)

        assert task.title == "Title"
        assert task.description == "Desc"

    def test_create_task_with_empty_title_raises_error(self):
        """Test that empty title raises error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with pytest.raises(InvalidTitleError):
            service.create_task(CreateTaskInput(title=""))

    def test_create_task_with_long_description_raises_error(self):
        """Test that long description raises error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with pytest.raises(InvalidDescriptionError):
            service.create_task(CreateTaskInput(title="Title", description="x" * 1001))


class TestTaskServiceList:
    """Test cases for TaskService.list_tasks."""

    def test_list_all_returns_all_tasks(self):
        """Test list_tasks with no filter returns all tasks."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task 1"))
        repo.save(Task(id=2, title="Task 2"))
        repo.save(Task(id=3, title="Task 3", completed=True))
        service = TaskService(repo)

        tasks = service.list_tasks()

        assert len(tasks) == 3

    def test_list_with_completed_filter(self):
        """Test list_tasks with completed=True filter."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task 1", completed=True))
        repo.save(Task(id=2, title="Task 2", completed=False))
        repo.save(Task(id=3, title="Task 3", completed=True))
        service = TaskService(repo)

        tasks = service.list_tasks(completed_filter=True)

        assert len(tasks) == 2
        assert all(t.completed for t in tasks)

    def test_list_with_pending_filter(self):
        """Test list_tasks with completed=False filter."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task 1", completed=True))
        repo.save(Task(id=2, title="Task 2", completed=False))
        repo.save(Task(id=3, title="Task 3", completed=True))
        service = TaskService(repo)

        tasks = service.list_tasks(completed_filter=False)

        assert len(tasks) == 1
        assert not tasks[0].completed


class TestTaskServiceComplete:
    """Test cases for TaskService.complete_task."""

    def test_complete_task(self):
        """Test completing an incomplete task."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task", completed=False))
        service = TaskService(repo)

        task = service.complete_task(1)

        assert task.completed is True

    def test_complete_nonexistent_task_raises_error(self):
        """Test completing non-existent task raises error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with pytest.raises(TaskNotFoundError):
            service.complete_task(999)

    def test_complete_already_completed_task_raises_error(self):
        """Test completing already completed task raises error."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task", completed=True))
        service = TaskService(repo)

        with pytest.raises(TaskAlreadyCompletedError):
            service.complete_task(1)


class TestTaskServiceDelete:
    """Test cases for TaskService.delete_task."""

    def test_delete_task(self):
        """Test deleting a task."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task"))
        service = TaskService(repo)

        service.delete_task(1)

        assert repo.get(1) is None
        assert repo.count() == 0

    def test_delete_nonexistent_task_raises_error(self):
        """Test deleting non-existent task raises error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with pytest.raises(TaskNotFoundError):
            service.delete_task(999)


class TestTaskServiceUpdate:
    """Test cases for TaskService.update_task."""

    def test_update_title(self):
        """Test updating task title."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Old Title"))
        service = TaskService(repo)

        task = service.update_task(1, UpdateTaskInput(title="New Title"))

        assert task.title == "New Title"

    def test_update_description(self):
        """Test updating task description."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task", description="Old Desc"))
        service = TaskService(repo)

        task = service.update_task(1, UpdateTaskInput(description="New Desc"))

        assert task.description == "New Desc"

    def test_update_title_and_description(self):
        """Test updating both title and description."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Old", description="Old"))
        service = TaskService(repo)

        task = service.update_task(
            1,
            UpdateTaskInput(title="New", description="New")
        )

        assert task.title == "New"
        assert task.description == "New"

    def test_update_nonexistent_task_raises_error(self):
        """Test updating non-existent task raises error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with pytest.raises(TaskNotFoundError):
            service.update_task(999, UpdateTaskInput(title="New"))

    def test_update_with_empty_title_raises_error(self):
        """Test updating with empty title raises error."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task"))
        service = TaskService(repo)

        with pytest.raises(InvalidTitleError):
            service.update_task(1, UpdateTaskInput(title=""))


class TestTaskServiceToggle:
    """Test cases for TaskService.toggle_task."""

    def test_toggle_incomplete_to_complete(self):
        """Test toggling incomplete task to complete."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task", completed=False))
        service = TaskService(repo)

        task = service.toggle_task(1)

        assert task.completed is True

    def test_toggle_complete_to_incomplete(self):
        """Test toggling complete task to incomplete."""
        repo = InMemoryTaskRepository()
        repo.save(Task(id=1, title="Task", completed=True))
        service = TaskService(repo)

        task = service.toggle_task(1)

        assert task.completed is False

    def test_toggle_nonexistent_task_raises_error(self):
        """Test toggling non-existent task raises error."""
        repo = InMemoryTaskRepository()
        service = TaskService(repo)

        with pytest.raises(TaskNotFoundError):
            service.toggle_task(999)
