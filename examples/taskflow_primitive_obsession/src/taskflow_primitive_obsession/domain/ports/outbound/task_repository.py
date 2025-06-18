from abc import ABC, abstractmethod

from taskflow_primitive_obsession.domain.entities.task import Task
from taskflow_primitive_obsession.domain.ports.outbound.task_repository import (
    AsyncRepository,
)


class AsyncTaskRepository(AsyncRepository[Task, str], ABC):
    """
    Repository interface for Task aggregate roots.

    This interface defines the contract for managing Task aggregates in a data store.
    It provides methods to find, save, delete, and retrieve all Task aggregates.
    """

    @abstractmethod
    async def find_by_id(self, task_id: str) -> Task | None:
        """
        Find a Task by its unique identifier.

        Args:
            task_id (str): The unique identifier of the Task.

        Returns:
            Task | None: The Task if found, otherwise None.
        """
        pass

    @abstractmethod
    async def save(self, task: Task) -> None:
        """
        Save a Task aggregate to the repository.

        Args:
            task (Task): The Task aggregate to save.
        """
        pass

    @abstractmethod
    async def delete(self, task: Task) -> None:
        """
        Delete a Task aggregate from the repository.

        Args:
            task (Task): The Task aggregate to delete.
        """
        pass

    @abstractmethod
    async def find_all(self) -> list[Task]:
        """
        Find all Tasks in the repository.

        Returns:
            list[Task]: All Tasks in the repository.
        """
        pass
