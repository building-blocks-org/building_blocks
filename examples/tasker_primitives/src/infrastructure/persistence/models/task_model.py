from __future__ import annotations

from uuid import UUID

from examples.tasker_primitives.src.domain.entities.task import Task
from examples.tasker_primitives.src.infrastructure.persistence.models.base import (
    MappedModel,
)


class TaskModel(MappedModel[Task, UUID]):
    """
    SQLAlchemy model for Task aggregate.

    This model maps the Task aggregate to a database table, providing
    methods to convert between the model and the domain entity.
    """

    __tablename__ = "tasks"

    id: UUID
    title: str
    description: str
    status: str

    def __init__(self, id: UUID, title: str, description: str, status: str) -> None:
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
