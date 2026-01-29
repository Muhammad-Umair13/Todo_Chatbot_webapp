"""Task service layer for business logic.

This service layer handles all task-related operations and enforces
user isolation by filtering all queries by user_id.

Constitution Principle III: All task operations enforce ownership
at the database level through user_id filtering.
"""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone
from ..models.task import Task, TaskCreate, TaskUpdate, TaskResponse

import logging
logger = logging.getLogger(__name__)


class TaskService:
    """Service class for handling task business logic."""

    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> TaskResponse:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            TaskResponse: The created task with all fields
        """
        # Create task instance with user_id from JWT
        task_dict = task_data.model_dump()
        task_dict["user_id"] = user_id  # Add user_id to the dict before validation
        task = Task.model_validate(task_dict)

        # Add to session and commit
        session.add(task)
        session.commit()
        logger.info(f"Created task id={task.id}, user_id={user_id}")

        # Return as TaskResponse schema
        return TaskResponse.model_validate(task)

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> TaskResponse | None:
        """
        Get a specific task by ID for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            TaskResponse: The requested task or None if not found
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if task:
            return TaskResponse.model_validate(task)
        return None

    @staticmethod
    def get_tasks(session: Session, user_id: str, completed: Optional[bool] = None) -> List[TaskResponse]:
        """
        Get all tasks for the specified user with optional completion filter.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            completed: Optional filter for completion status (None = all tasks)

        Returns:
            List[TaskResponse]: List of tasks matching the criteria
        """
        statement = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            statement = statement.where(Task.completed == completed)

        statement = statement.order_by(Task.created_at.desc())

        tasks = session.exec(statement).all()

        return [TaskResponse.model_validate(task) for task in tasks]

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """
        Update a specific task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user updating the task
            task_update: Update data

        Returns:
            TaskResponse: The updated task or None if not found
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task not found for update: id={task_id}, user_id={user_id}")
            return None

        # Update the task with the provided data
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if value is not None:
                setattr(task, field, value)

        # Update the updated_at timestamp
        task.updated_at = datetime.now(timezone.utc)

        # Commit changes and refresh
        session.add(task)
        session.commit()
        logger.info(f"Updated task id={task.id}, user_id={user_id}")

        return TaskResponse.model_validate(task)

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Delete a specific task for the specified user.
        """
        logger.info(f"Delete attempt: task_id={task_id}, user_id={user_id}")


        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task not found: id={task_id}, user_id={user_id}")
            return False

        session.delete(task)
        session.commit()

        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[TaskResponse]:
        """
        Toggle the completion status of a specific task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the user toggling the task

        Returns:
            TaskResponse: The updated task or None if not found
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            logger.warning(f"Task not found for toggle: id={task_id}, user_id={user_id}")
            return None

        # Toggle the completion status
        task.completed = not task.completed
        task.updated_at = datetime.now(timezone.utc)

        # Commit changes and refresh
        session.add(task)
        session.commit()
        logger.info(f"Toggled task id={task.id}, user_id={user_id}, completed={task.completed}")

        return TaskResponse.model_validate(task)


__all__ = ["TaskService"]