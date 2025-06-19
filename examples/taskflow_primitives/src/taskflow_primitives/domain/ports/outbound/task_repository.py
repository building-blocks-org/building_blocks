from abc import ABC, abstractmethod
from typing import Optional

from building_blocks.domain.ports.outbound.repository import AsyncRepository
from taskflow_primitives.domain.entities.task import Task


class TaskRepository(AsyncRepository[Task, str], ABC):
    """
    Repository interface for Task entities.

    This repository provides methods to interact with Task entities,
    including saving, deleting, and retrieving tasks by their ID.
    """

    @abstractmethod
    async def save(self, aggregate: Task) -> None:
        """
        Save a Task entity to the repository.

        :param task: The Task entity to save.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def find_by_id(self, aggregate_id: str) -> Optional[Task]:
        """
        Retrieve a Task entity by its ID.

        :param id_: The ID of the Task entity.
        :return: The Task entity if found, otherwise None.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def find_all(self) -> list[Task]:
        """
        Retrieve all Task entities from the repository.

        :return: A list of all Task entities.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def delete(self, aggregate_id: str) -> None:
        """
        Delete a Task entity from the repository.

        :param task: The Task entity to delete.
        """
        raise NotImplementedError("Method not implemented")
