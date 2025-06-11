"""
Convenience repository classes for common patterns.

This module provides convenience base classes following industry standard naming
conventions.
Most repositories work with UUID-based aggregates, so these classes provide simpler
interfaces.
"""

from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from building_blocks.domain.ports.outbound.read_only_repository import (
    ReadOnlyRepository,
)
from building_blocks.domain.ports.outbound.repository import Repository
from building_blocks.domain.ports.outbound.write_only_repository import (
    WriteOnlyRepository,
)

TAggregateRoot = TypeVar("TAggregateRoot")


class UUIDRepository(Repository[TAggregateRoot, UUID], Generic[TAggregateRoot]):
    """
    Convenience base class for UUID-based repositories.

    Most aggregates use UUID as their identifier, so this provides
    a simpler interface following industry standard naming conventions
    used by Spring Data, .NET Entity Framework, and other major frameworks.

    Example:
        >>> from building_blocks.domain.aggregate_root import AggregateRoot
        >>>
        >>> class Order(AggregateRoot[UUID]):
        ...     pass
        >>>
        >>> class OrderRepository(UUIDRepository[Order]):
        ...     def find_by_id(self, order_id: UUID) -> Order | None:
        ...         # Implementation
        ...         pass
        ...
        ...     def save(self, order: Order) -> None:
        ...         # Implementation
        ...         pass
        ...
        ...     def delete(self, order: Order) -> None:
        ...         # Implementation
        ...         pass
        ...
        ...     def find_all(self) -> list[Order]:
        ...         # Implementation
        ...         pass
        ...
        ...     # Add aggregate-specific methods
        ...     def find_by_customer_id(self, customer_id: str) -> list[Order]:
        ...         # Business-specific query
        ...         pass
    """

    pass


class UUIDReadOnlyRepository(
    ReadOnlyRepository[TAggregateRoot, UUID], Generic[TAggregateRoot]
):
    """
    Convenience base class for UUID-based read-only repositories.

    Perfect for CQRS query-side repositories that work with UUID-based aggregates.
    Follows industry standard naming from CQRS community.

    Example:
        >>> class OrderQueryRepository(UUIDReadOnlyRepository[Order]):
        ...     def find_by_id(self, order_id: UUID) -> Order | None:
        ...         # Query implementation - read from read model
        ...         pass
        ...
        ...     def find_all(self) -> list[Order]:
        ...         # Query implementation
        ...         pass
        ...
        ...     # Add query-optimized methods
        ...     def find_by_customer_email(self, email: str) -> list[Order]:
        ...         # Optimized for read scenarios
        ...         pass
        ...
        ...     def get_order_statistics(self) -> dict[str, int]:
        ...         # Complex analytical queries
        ...         pass
    """

    pass


class UUIDWriteOnlyRepository(
    WriteOnlyRepository[TAggregateRoot], Generic[TAggregateRoot]
):
    """
    Convenience base class for UUID-based write-only repositories.

    Perfect for CQRS command-side repositories that work with UUID-based aggregates.
    Follows industry standard naming from CQRS community.

    Example:
        >>> class OrderCommandRepository(UUIDWriteOnlyRepository[Order]):
        ...     def save(self, order: Order) -> None:
        ...         # Command implementation - save to event store
        ...         # Publish domain events
        ...         pass
        ...
        ...     def delete(self, order: Order) -> None:
        ...         # Command implementation - mark as deleted
        ...         pass
    """

    pass
