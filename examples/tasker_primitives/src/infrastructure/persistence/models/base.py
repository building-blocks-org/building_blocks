from __future__ import annotations

import datetime
import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# === Declarative Base ===


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy v2+."""

    pass


# === UTC timestamp generator ===

UTC = datetime.timezone.utc


def now_utc() -> datetime.datetime:
    return datetime.datetime.now(tz=UTC)


# === TimestampedBase ===


class TimestampedBase(Base):
    """
    Abstract base class for models with created_at / updated_at columns.
    Intended for primitive-obsessed usage (not using VOs).
    """

    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, nullable=False
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc, nullable=False
    )


# === Typevars for generic base model ===

TEntity = TypeVar("TEntity")
TId = TypeVar("TId", bound=uuid.UUID)  # assumes all IDs are UUIDs


# === MappedModel ===


class MappedModel(ABC, Generic[TEntity, TId]):
    """
    Abstract base class for mapped models with a primitive UUID primary key.

    Intended for use in designs where domain entities are not rich value objects,
    but rather raw types or anemic models. This interface standardizes conversion.
    """

    __abstract__ = True

    id: Mapped[TId]

    @abstractmethod
    def to_entity(self) -> TEntity:
        """Convert this ORM model to its corresponding domain-like entity."""
        pass

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: TEntity) -> MappedModel[TEntity, TId]:
        """Build an ORM model from a raw domain-like entity."""
        pass
