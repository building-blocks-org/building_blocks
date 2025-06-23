from __future__ import annotations

import uuid

from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from examples.tasker_primitives.src.domain.entities.task import Task
from examples.tasker_primitives.src.infrastructure.persistence.models.base import (
    MappedModel,
    TimestampedBase,
)


class TaskModel(TimestampedBase, MappedModel[Task, uuid.UUID]):
    """
    SQLAlchemy model for Task aggregate.

    This model maps the Task aggregate to a database table, providing
    methods to convert between the model and the domain entity.
    """

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str]

    def __init__(
        self, id: uuid.UUID, title: str, description: str, status: str
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.status = status

    def to_entity(self) -> Task:
        return Task(
            task_id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            version=0,  # Assuming version is not stored in the model
        )

    @classmethod
    def from_entity(cls, entity: Task) -> TaskModel:
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
        )
