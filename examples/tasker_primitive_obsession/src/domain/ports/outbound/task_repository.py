from abc import ABC, abstractmethod
from typing import List, Optional

from building_blocks.domain.ports.outbound.repository import AsyncRepository
from examples.tasker_primitive_obsession.src.domain.entities.task import Task


class TaskRepository(AsyncRepository[Task, int], ABC):
    """
    Repository interface for Task aggregate.

    This interface defines the methods for managing Task aggregates in a
    persistent storage. It extends AsyncRepository to provide asynchronous
    operations for creating, updating, and retrieving tasks.
    """

    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[Task]:
        """
        Find a Task aggregate by its ID.
        Args:
            id (int): The unique identifier of the task.
        Returns:
            Optional[Task]: The Task aggregate if found, otherwise None.
        """
        pass

    @abstractmethod
    async def save(self, aggregate: Task) -> None:
        """
        Save a Task aggregate to the repository.

        This method handles both create and update operations.
        If the Task already exists, it updates the existing record.
        If it does not exist, it creates a new record.
        It is expected that the Task aggregate has a valid ID before calling this
        method.
        If the ID is None, it should be set to a new unique identifier by the Repository
        implementation.

        Args:
            aggregate (Task): The Task aggregate to save.

        Returns:
            None: This method does not return a value. It raises an exception if the
            save operations fails, such as due to a database error or validation issue.

        """
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        """
        Attempt to delete Task aggregate by its ID.

        Args:
            id (int): The unique identifier of the task to delete.

        """
        pass

    @abstractmethod
    async def find_all(self) -> List[Task]:
        """
        Find all Task aggregates in the repository.

        Returns:
            List[Task]: A list of all Task aggregates.
        """
        pass
