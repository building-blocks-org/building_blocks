from __future__ import annotations

import datetime
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

    def __init__(
        self,
        task_id: UUID,
        title: str,
        description: str,
        due_date: datetime.date,
        status: str = "todo",
        version: int = 0,
    ) -> None:
        super().__init__(task_id, version)
        self._title = title
        self._description = description
        self._due_date = due_date
        self._status = status

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"    id={self._id!r},\n"
            f"    title={self._title!r},\n"
            f"    description={self._description!r},\n"
            f"    status={self._status!r}\n"
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
