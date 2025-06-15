"""
Unit of Work interface for managing transactions.

The Unit of Work pattern maintains a list of objects affected by a business
transaction and coordinates writing out changes and resolving concurrency problems.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class AsyncUnitOfWork(ABC):
    """
    Unit of Work interface for managing transactions.

    The Unit of Work pattern maintains a list of objects affected by a business
    transaction and coordinates writing out changes and resolving concurrency problems.

    This is particularly useful when multiple repositories need to participate
    in a single transaction to maintain consistency.
    """

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit all changes in the unit of work.

        This should:
        - Persist all registered changes
        - Publish domain events
        - Handle transaction coordination

        Raises:
            UnitOfWorkException: If commit fails
        """

    @abstractmethod
    async def rollback(self) -> None:
        """
        Rollback all changes in the unit of work.

        Raises:
            UnitOfWorkException: If rollback fails
        """


class SyncUnitOfWork(ABC):
    """
    Unit of Work interface for managing transactions.

    The Unit of Work pattern maintains a list of objects affected by a business
    transaction and coordinates writing out changes and resolving concurrency problems.

    This is particularly useful when multiple repositories need to participate
    in a single transaction to maintain consistency.
    """

    @abstractmethod
    def commit(self) -> None:
        """
        Commit all changes in the unit of work.

        This should:
        - Persist all registered changes
        - Publish domain events
        - Handle transaction coordination

        Raises:
            UnitOfWorkException: If commit fails
        """

    @abstractmethod
    def rollback(self) -> None:
        """
        Rollback all changes in the unit of work.

        Raises:
            UnitOfWorkException: If rollback fails
        """
