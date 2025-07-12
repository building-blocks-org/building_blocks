from abc import ABC, abstractmethod
from uuid import UUID

from building_blocks.domain.ports.outbound.repository import AsyncRepository
from examples.tasker_primitives.src.domain.entities.task import Task


class TaskRepository(AsyncRepository[Task, UUID], ABC):
    """
    Repository interface for Task aggregate.

    This interface defines the methods for managing Task aggregates in a
    persistent storage. It extends AsyncRepository to provide asynchronous
    operations for creating, updating, and retrieving tasks.
    """

    @abstractmethod
    async def find_by_id(self, task_id: UUID) -> Optional[Task]:
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
        Find all Task aggregates in the repository.

        Returns:
            list[Task]: A list of all Task aggregates.
        """
        pass
