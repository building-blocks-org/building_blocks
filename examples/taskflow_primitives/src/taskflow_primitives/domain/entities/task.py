from __future__ import annotations

from uuid import uuid4

from building_blocks.domain.aggregate_root import AggregateRoot


class Task(AggregateRoot[str]):
    def __init__(
        self,
        id_: str,
        title: str,
        description: str,
        due_date: str,
        priority: int,
        status: str = "pending",
        tags: list[str] | None = None,
    ) -> None:
        self.id_ = id_
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.tags = tags if tags is not None else []

    @classmethod
    def create_pending(
        cls,
        title: str,
        description: str,
        due_date: str,
        priority: int,
        tags: list[str] | None = None,
    ) -> Task:
        id_ = uuid4().hex
        return cls(id_, title, description, due_date, priority, "pending", tags)

    def mark_completed(self) -> None:
        self.status = "completed"
