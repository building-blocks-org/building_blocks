import datetime

from sqlalchemy import DateTime, event, func
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, Mapper, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
        onupdate=lambda: datetime.datetime.now(datetime.timezone.utc),
    )


@event.listens_for(BaseModel, "before_update", propagate=True)
def receive_before_update(
    mapper: Mapper, connection: Connection, target: BaseModel
) -> None:
    target.updated_at = datetime.datetime.now(datetime.timezone.utc)
