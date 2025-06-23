from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from examples.tasker_primitives.src.domain.entities.task import Task
from examples.tasker_primitives.src.domain.ports.outbound.task_repository import (
    TaskRepository,
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
        values = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "due_date": task.due_date,
            "version": task.version,
        }

        dialect_name = self._session.bind.dialect.name

        if dialect_name == "postgresql":
            insert_stmt = pg_insert(TaskModel.__table__)
        elif dialect_name == "sqlite":
            insert_stmt = sqlite_insert(TaskModel.__table__)
        else:
            raise NotImplementedError(f"Upsert not supported for {dialect_name}")

        upsert_stmt = insert_stmt.values(**values).on_conflict_do_update(
            index_elements=["id"],
            set_={k: getattr(insert_stmt.excluded, k) for k in values if k != "id"},
        )

        await self._session.execute(upsert_stmt)
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
