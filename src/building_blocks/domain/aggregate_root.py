"""
AggregateRoot module for Domain-Driven Design.

This module provides the AggregateRoot base class for implementing domain aggregates
following Domain-Driven Design (DDD) principles, using Vaughn Vernon's approach.
"""

from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from building_blocks.domain.entity import Entity
from building_blocks.domain.messages.event import Event

TId = TypeVar("TId")


class AggregateRoot(Entity[TId], Generic[TId], ABC):
    """
    Base class for all domain aggregate roots.

    An aggregate root is the only entry point to an aggregate. It ensures consistency
    and business rules within the aggregate boundary. It also manages domain events
    that represent important business occurrences.

    This implementation follows Vaughn Vernon's approach from
    "Implementing Domain-Driven Design".
    """

    def __init__(self, aggregate_id: TId, version: int = 0) -> None:
        """
        Initialize the aggregate root.

        Args:
            aggregate_id: Unique identifier for this aggregate
            version: Version number for optimistic concurrency control
        """
        super().__init__(aggregate_id)
        self._version: int = version  # ✅ Explicit type annotation
        self._uncommitted_events: list[Event] = []

    @property
    def version(self) -> int:
        """
        Get the current version of this aggregate.

        Used for optimistic concurrency control to prevent conflicting updates.

        Returns:
            int: The current version number
        """
        return self._version  # ✅ Make sure this returns the right attribute

    def uncommitted_changes(self) -> list[Event]:
        """
        Get the uncommitted domain events raised by this aggregate.

        Returns a copy to prevent external modification.
        Following Vaughn Vernon's naming convention.

        Returns:
            list[Event]: Copy of uncommitted domain events
        """
        return self._uncommitted_events.copy()

    def record_event(self, domain_event: Event) -> None:
        """
        Record a domain event to be published.

        This is the primary method for recording domain events when significant
        business events occur. Following Vaughn Vernon's naming convention.

        Args:
            domain_event: The domain event to record
        """
        self._uncommitted_events.append(domain_event)

    def mark_changes_as_committed(self) -> None:
        """
        Mark all uncommitted changes as committed and clear them.

        This method should be called after events have been successfully
        published and the aggregate has been persisted.
        Following Vaughn Vernon's naming convention.
        """
        self._uncommitted_events.clear()
        self._increment_version()

    def _increment_version(self) -> None:
        """
        Increment the aggregate version.

        Protected method to be called when the aggregate state changes.
        Useful for optimistic concurrency control.
        """
        self._version += 1
