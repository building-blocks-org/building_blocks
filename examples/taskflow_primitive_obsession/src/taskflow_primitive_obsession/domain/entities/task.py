from datetime import datetime
from typing import Optional

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
        assigned_to_email: Optional[str] = None,
    ):
        super().__init__(id_)
        self._name = name
        self._description = description
        self._priority = priority
        self._assigned_to_email = assigned_to_email
        self._status = status
        self._due_date = due_date

    def mark_as_completed(self):
        self.status = "completed"

    def __str__(self):
        return f"""Task(
        name={self._name},
        description={self._description},
        priority={self._priority},
        status={self._status},
        due_date={self._due_date},
    )"""
