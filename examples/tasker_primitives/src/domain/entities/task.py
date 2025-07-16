from __future__ import annotations

import datetime
from typing import List, Optional
from uuid import UUID

from building_blocks.domain.aggregate_root import AggregateRoot


class Task(AggregateRoot[UUID]):
    """
    Represents a task in the domain model.
    This class extends AggregateRoot to provide a unique identifier and versioning
    for optimistic concurrency control.
    It includes properties for task description and status, along with methods to
    mark the task as done, todo, or in progress.
    Args:
        task_id (UUID): Unique identifier for the task.
        title (str): Title of the task.
        description (str): Description of the task.
        status (str): Current status of the task, default is "todo".
        version (int): Version number for optimistic concurrency control.
    """

    """Task Statuses"""
    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_BLOCKED = "blocked"
    STATUS_CANCELLED = "cancelled"
    STATUS_REVIEW = "review"
    STATUS_TESTING = "testing"

    """Task Priorities"""
    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_URGENT = "urgent"
    PRIORITY_CRITICAL = "critical"

    """Progress Range"""
    MIN_PROGRESS = 0
    MAX_PROGRESS = 100

    def __init__(
        self,
        task_id: UUID,
        title: str,
        description: str,
        due_date: datetime.date,
        status: str = "todo",
        priority: str = PRIORITY_MEDIUM,
        tags: Optional[List[str]] = None,
        progress: int = 0,
        assignee_email: Optional[str] = None,
        version: int = 0,
    ) -> None:
        # Validate priority
        valid_priorities = [
            self.PRIORITY_LOW,
            self.PRIORITY_MEDIUM,
            self.PRIORITY_HIGH,
            self.PRIORITY_URGENT,
            self.PRIORITY_CRITICAL,
        ]
        if priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")

        # Validate progress
        if not self.MIN_PROGRESS <= progress <= self.MAX_PROGRESS:
            raise ValueError(
                f"Progress must be between {self.MIN_PROGRESS} and {self.MAX_PROGRESS}"
            )

        # Validate assignee email if provided
        if assignee_email is not None and "@" not in assignee_email:
            raise ValueError("Invalid email format")

        # Validate tags
        if tags is not None:
            if not all(isinstance(tag, str) and tag.strip() for tag in tags):
                raise ValueError("All tags must be non-empty strings")

        # Validate due date
        if due_date < datetime.date.today():
            raise ValueError("Due date cannot be in the past")

        super().__init__(task_id, version)
        self._title = title
        self._description = description

        self._due_date = due_date

        self._status = status
        self._priority = priority
        self._tags = tags if tags is not None else []
        self._progress = progress
        self._assignee_email = assignee_email

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"    id={self._id!r},\n"
            f"    title={self._title!r},\n"
            f"    description={self._description!r},\n"
            f"    due_date={self._due_date!r},\n"
            f"    status={self._status!r},\n"
            f"    priority={self._priority!r},\n"
            f"    tags={self._tags!r},\n"
            f"    progress={self._progress!r},\n"
            f"    assignee_email={self._assignee_email!r}\n"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash((self._id, self._description, self._status, self._version))

    @property
    def title(self) -> str:
        """
        Get the title of the task.

        Returns:
            str: The title of the task.
        """
        return self._title

    @property
    def description(self) -> str:
        """
        Get the description of the task.

        Returns:
            str: The description of the task.
        """
        return self._description

    @property
    def status(self) -> str:
        """
        Get the current status of the task.

        Returns:
            str: The current status of the task.
        """
        return self._status

    @property
    def due_date(self) -> datetime.date:
        """
        Get the due date of the task.

        Returns:
            datetime.date: The due date of the task.
        """
        return self._due_date

    @property
    def priority(self) -> str:
        """
        Get the priority of the task.

        Returns:
            str: The priority of the task.
        """
        return self._priority

    @property
    def tags(self) -> List[str]:
        """
        Get the tags associated with the task.

        Returns:
            List[str]: The tags of the task.
        """
        return self._tags.copy()

    @property
    def progress(self) -> int:
        """
        Get the progress percentage of the task.

        Returns:
            int: The progress percentage (0-100).
        """
        return self._progress

    @property
    def assignee_email(self) -> Optional[str]:
        """
        Get the email of the assigned user.

        Returns:
            str: The assignee's email address.
        """
        return self._assignee_email

    def mark_as_done(self) -> None:
        self._status = self.STATUS_DONE
        self._progress = self.MAX_PROGRESS100

    def start_task(self) -> None:
        if self._status == self.STATUS_TODO:
            self._status = self.STATUS_IN_PROGRESS
            self._progress = 0
        else:
            raise ValueError("Task must be in 'todo' status to start.")

    def assign_to(self, email: str) -> None:
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        self._assignee_email = email

    def add_tag(self, tag: str) -> None:
        if not tag or not isinstance(tag, str) or not tag.strip():
            raise ValueError("Tag must be a non-empty string")
        if tag not in self._tags:
            self._tags.append(tag)
