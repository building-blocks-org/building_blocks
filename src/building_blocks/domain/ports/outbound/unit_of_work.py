"""
Unit of Work interface for managing transactions.

The Unit of Work pattern maintains a list of objects affected by a business
transaction and coordinates writing out changes and resolving concurrency problems.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    """
    Unit of Work interface for managing transactions.

    The Unit of Work pattern maintains a list of objects affected by a business
    transaction and coordinates writing out changes and resolving concurrency problems.

    This is particularly useful when multiple repositories need to participate
    in a single transaction to maintain consistency.

    Example:
        >>> class DatabaseUnitOfWork(UnitOfWork):
        ...     def __init__(self, session):
        ...         self._session = session
        ...         self._new = set()
        ...         self._dirty = set()
        ...         self._removed = set()
        ...
        ...     def register_new(self, aggregate: AggregateRoot) -> None:
        ...         self._new.add(aggregate)
        ...
        ...     def commit(self) -> None:
        ...         # Persist all changes in a transaction
        ...         self._session.commit()
        ...
        ...     def rollback(self) -> None:
        ...         self._session.rollback()
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
