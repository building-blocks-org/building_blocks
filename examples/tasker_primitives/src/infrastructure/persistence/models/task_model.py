from __future__ import annotations

import datetime
import uuid

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from examples.tasker_primitives.src.domain.entities.task import Task
from examples.tasker_primitives.src.infrastructure.persistence.models.base import (
    OrmModel,
)


class TaskModel(OrmModel[Task, uuid.UUID]):
    """
    SQLAlchemy model for Task aggregate.

    This model maps the Task aggregate to a database table, providing
    methods to convert between the model and the domain entity.
    """

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    status: Mapped[str]
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)

    def __init__(
        self,
        id: uuid.UUID,
        title: str,
        description: str,
        status: str,
        due_date: datetime.date,
    ) -> None:
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.due_date = due_date

    def to_entity(self) -> Task:
        return Task(
            task_id=self.id,
            title=self.title,
            description=self.description,
            status=self.status,
            due_date=self.due_date,
            version=0,  # Assuming version is not stored in the model
        )

    @classmethod
    def from_entity(cls, entity: Task) -> TaskModel:
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            due_date=entity.due_date,
        )
