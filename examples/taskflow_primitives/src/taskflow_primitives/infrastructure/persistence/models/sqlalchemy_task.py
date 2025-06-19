from __future__ import annotations

import datetime

from sqlalchemy import JSON, Date
from sqlalchemy.orm import Mapped, mapped_column

from taskflow_primitives.domain.entities.task import Task
from taskflow_primitives.infrastructure.persistence.models.base import BaseModel


class SQLAlchemyTask(BaseModel):
    __tablename__ = "tasks"

    id_: Mapped[str] = mapped_column(primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    due_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    priority: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default="pending")
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    @classmethod
    def from_entity(cls, entity: Task) -> SQLAlchemyTask:
        return cls(
            id_=entity._id,
            title=entity.title,
            description=entity.description,
            due_date=entity.due_date,
            priority=entity.priority,
            status=entity.status,
            tags=entity.tags,
        )

    def to_entity(self) -> Task:
        return Task(
            id_=self.id_,
            title=self.title,
            description=self.description,
            due_date=self.due_date,
            priority=self.priority,
            status=self.status,
            tags=self.tags,
        )
