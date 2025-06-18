from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from building_blocks.domain.aggregate_root import AggregateRoot


class Task(AggregateRoot[str]):
    def __init__(
        self,
        id_: str,
        name: str,
        description: str,
        priority: str,
        due_date: datetime,
        status: str,
        assigned_to_email: str | None = None,
    ):
        super().__init__(id_)
        self._name = name
        self._description = description
        self._priority = priority
        self._assigned_to_email = assigned_to_email
        self._status = status
        self._due_date = due_date

    @classmethod
    def create_pending(
        cls,
        name: str,
        description: str,
        priority: str,
        due_date: datetime,
        assigned_to_email: str | None = None,
    ):
        """
        Factory method to create a new pending task.

        Args:
            name (str): Name of the task
            description (str): Description of the task
            priority (str): Priority level of the task
            due_date (datetime): Due date for the task
            assigned_to_email (Optional[str]): Email of the user assigned to the task

        Returns:
            Task: A new Task instance in pending state
        """
        id_ = uuid4().hex
        return Task(
            id_, name, description, priority, due_date, "pending", assigned_to_email
        )

    def __str__(self) -> str:
        return f"""Task(
        name={self._name},
        description={self._description},
        priority={self._priority},
        status={self._status},
        due_date={self._due_date},
    )"""

    def mark_as_done(self) -> None:
        self.status = "completed"
