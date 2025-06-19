from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow_primitives.domain.entities.task import Task
from taskflow_primitives.domain.ports.outbound.task_repository import TaskRepository
from taskflow_primitives.infrastructure.persistence.models.sqlalchemy_task import (
    SQLAlchemyTask,
)


class SQLAlchemyTaskRepository(TaskRepository):
    """
    SQLAlchemy implementation of the TaskRepository interface.

    This class provides methods to interact with Task entities using SQLAlchemy ORM.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the SQLAlchemyTaskRepository with an AsyncSession.

        :param session: The SQLAlchemy AsyncSession to use for database operations.
        """
        self._session = session

    async def save(self, aggregate: Task) -> None:
        """
        Save a Task entity to the database.

        :param aggregate: The Task entity to save.
        """
        # Implementation for saving the task using SQLAlchemy
        model = SQLAlchemyTask.from_entity(aggregate)
        async with self._session.begin():
            await self._session.merge(model)
            await self._session.flush()  # Ensure the entity is persisted

    async def find_by_id(self, aggregate_id: str) -> Optional[Task]:
        """
        Retrieve a Task entity by its ID.

        :param aggregate_id: The ID of the Task entity.
        :return: The Task entity if found, otherwise None.
        """
        # Implementation for finding a task by ID using SQLAlchemy
        result = await self._session.execute(
            select(SQLAlchemyTask).where(SQLAlchemyTask.id_ == aggregate_id)
        )

        task_model = result.scalar_one_or_none()

        return task_model.to_entity() if task_model else None

    async def find_all(self) -> list[Task]:
        """
        Retrieve all Task entities from the database.

        :return: A list of all Task entities.
        """
        # Implementation for finding all tasks using SQLAlchemy
        result = await self._session.execute(select(SQLAlchemyTask))

        task_models = result.scalars().all()

        return [task_model.to_entity() for task_model in task_models]

    async def delete(self, aggregate_id: str) -> None:
        """
        Delete a Task entity from the database.

        :param aggregate_id: The ID of the Task entity to delete.
        """
        # Implementation for deleting a task using SQLAlchemy
        await self._session.execute(
            delete(SQLAlchemyTask).where(SQLAlchemyTask.id_ == aggregate_id)
        )
        await self._session.flush()
