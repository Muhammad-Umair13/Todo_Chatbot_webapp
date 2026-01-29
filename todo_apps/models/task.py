"""Task data model.

T-004: Create Task domain model in src/models/task.py
Spec Ref: sp.specify §Task Entity, sp.data-model.md §Task Entity
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Self


class Priority(str, Enum):
    """Priority levels for tasks."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Recurrence(str, Enum):
    """Recurrence patterns for tasks."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique auto-incrementing identifier for the task.
        title: Brief description of what needs to be done (1-200 chars).
        description: Detailed information about the task (max 1000 chars).
        completed: Whether the task has been finished.
        priority: Task priority level (high/medium/low).
        tags: List of tags/categories for the task.
        due_date: Optional deadline for the task.
        recurrence: Recurrence pattern (none, daily, weekly, monthly).
        created_at: Timestamp when the task was created.
        updated_at: Timestamp when the task was last modified.
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    due_date: datetime | None = None
    recurrence: Recurrence = Recurrence.NONE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_title(self, new_title: str) -> None:
        """Update task title and set updated_at timestamp.

        Args:
            new_title: The new title for the task.
        """
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

    def set_priority(self, priority: Priority) -> None:
        """Set task priority.

        Args:
            priority: The new priority level.
        """
        self.priority = priority
        self.updated_at = datetime.now()

    def add_tag(self, tag: str) -> None:
        """Add a tag to the task.

        Args:
            tag: The tag to add.
        """
        tag = tag.lower().strip()
        if tag and tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task.

        Args:
            tag: The tag to remove.
        """
        tag = tag.lower().strip()
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now()

    def set_tags(self, tags: list[str]) -> None:
        """Set all tags for the task.

        Args:
            tags: List of tags to set.
        """
        self.tags = [t.lower().strip() for t in tags if t.strip()]
        self.updated_at = datetime.now()

    def set_due_date(self, due_date: datetime | None) -> None:
        """Set the due date for the task.

        Args:
            due_date: The due date, or None to clear it.
        """
        self.due_date = due_date
        self.updated_at = datetime.now()

    def set_recurrence(self, recurrence: Recurrence) -> None:
        """Set the recurrence pattern for the task.

        Args:
            recurrence: The recurrence pattern.
        """
        self.recurrence = recurrence
        self.updated_at = datetime.now()

    def has_tag(self, tag: str) -> bool:
        """Check if task has a specific tag.

        Args:
            tag: The tag to check.

        Returns:
            True if the task has the tag, False otherwise.
        """
        return tag.lower().strip() in self.tags

    def matches_keyword(self, keyword: str) -> bool:
        """Check if task matches a keyword in title or description.

        Args:
            keyword: The keyword to search for.

        Returns:
            True if the keyword is found in title or description.
        """
        keyword_lower = keyword.lower()
        return (
            keyword_lower in self.title.lower() or
            keyword_lower in self.description.lower()
        )
