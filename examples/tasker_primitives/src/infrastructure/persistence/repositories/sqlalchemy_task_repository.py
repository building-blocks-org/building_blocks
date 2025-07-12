from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from examples.tasker_primitives.src.domain.entities.task import Task
from examples.tasker_primitives.src.domain.ports.outbound.task_repository import (
    TaskRepository,
)
from examples.tasker_primitives.src.infrastructure.persistence.helpers import (
    build_upsert_statement,
)
from examples.tasker_primitives.src.infrastructure.persistence.models import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    """
    SQLAlchemy implementation of the TaskRepository interface.

    This class provides methods to interact with the database for Task aggregates,
    including finding, saving, and deleting tasks.

    Note: This is a placeholder for the actual implementation.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the repository with a database session.

        Args:
            session: SQLAlchemy session for database operations.
        """
        self._session = session

    async def save(self, task: Task) -> None:
        values = self._build_values(task)

        dialect_name = self._session.bind.dialect.name

        upsert_statement = build_upsert_statement(
            dialect_name, TaskModel.__table__, values
        )

        await self._session.execute(upsert_statement)
        await self._session.commit()

    async def find_all(self) -> List[Task]:
        statement = select(TaskModel)
        result = await self._session.execute(statement)
        models = result.scalars().all()
        return [model.to_entity() for model in models]

    async def find_by_id(self, task_id: UUID) -> Optional[Task]:
        model = await self._session.get(TaskModel, task_id)

        if model:
            return model.to_entity()
        return None

    async def delete(self, task: Task) -> None:
        model = await self._session.get(TaskModel, task.id)

        if model:
            await self._session.delete(model)
            await self._session.commit()
        else:
            raise ValueError(f"Task with id {task.id} not found")

    def _build_values(self, task: Task) -> dict:
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date,
            "version": task.version,
        }
