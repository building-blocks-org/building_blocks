from __future__ import annotations

import datetime
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# -- SQLAlchemy Base --


class Base(DeclarativeBase):
    """Declarative base for SQLAlchemy v2+."""

    pass


# -- Utility: UTC timestamp generator --

UTC = datetime.timezone.utc


def now_utc() -> datetime.datetime:
    return datetime.datetime.now(tz=UTC)


# -- Timestamp Mixin (primitive-aware) --


class TimestampedBase(Base):
    """Abstract base for models with UUID PK and timestamp tracking."""

    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=now_utc, onupdate=now_utc, nullable=False
    )


# -- Typevars --

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


# -- MappedModel (primitive ID, no VO) --


class MappedModel(ABC, Generic[TEntity, TId]):
    """
    Base class for mapped models with primitive UUID primary key.
    Intended for primitive-obsessed designs.
    """

    __abstract__ = True

    id: Mapped[TId]

    @abstractmethod
    def to_entity(self) -> TEntity:
        """
        Convert the mapped model to a domain-like entity (dict or raw type).
        """
        pass

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: TEntity) -> MappedModel[TEntity, TId]:
        """
        Build the mapped model from a primitive-structured entity.
        """
        pass
