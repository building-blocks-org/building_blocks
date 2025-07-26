from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from building_blocks.domain.ports.outbound.repository import AsyncRepository
from examples.tasker_primitive_obsession.src.domain.entities.user import User


class UserRepository(AsyncRepository[User, UUID], ABC):
    """
    Repository interface for User aggregate.

    This interface defines the methods for managing User aggregates in a
    persistent storage. It extends AsyncRepository to provide asynchronous
    operations for creating, updating, and retrieving users.
    """

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> None:
        """
        Save a User aggregate to the repository.

        Args:
            user (User): The User aggregate to save.
        """
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        """
        Delete a User aggregate from the repository.

        Args:
            user (User): The User aggregate to delete.
        """
        pass

    @abstractmethod
    async def find_all(self) -> List[User]:
        """
        Find all User aggregates in the repository.

        Returns:
            List[User]: A List of all User aggregates.
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Find a User aggregate by email.
        This method does no

        Args:
            email (str): The email address of the user.

        Returns:
            Optional[User]: The User aggregate if found, otherwise None.
        """
        pass
