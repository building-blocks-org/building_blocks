import datetime
import time

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from taskflow_primitives.infrastructure.persistence.models.base import BaseModel


def ensure_utc(dt: datetime.datetime) -> datetime.datetime:
    """Ensure a datetime is offset-aware in UTC."""
    if dt.tzinfo is None:
        # Assume naive datetimes are in UTC
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


class DummyModel(BaseModel):
    __tablename__ = "dummy"

    id: Mapped[str] = mapped_column(primary_key=True)


class TestBaseModel:
    @pytest.mark.asyncio
    async def test_constructor_when_called_then_created_at_is_populated(
        self, async_session: AsyncSession
    ) -> None:
        dummy = DummyModel(id="dummy_id")
        async_session.add(dummy)

        await async_session.commit()

        assert isinstance(dummy.created_at, datetime.datetime)
        assert dummy.created_at.tzinfo is not None

    @pytest.mark.asyncio
    async def test_constructor_when_called_then_updated_at_is_populated(
        self, async_session: AsyncSession
    ) -> None:
        dummy = DummyModel(id="dummy_id2")
        async_session.add(dummy)

        await async_session.commit()

        assert isinstance(dummy.updated_at, datetime.datetime)
        assert dummy.updated_at.tzinfo is not None

    @pytest.mark.asyncio
    async def test_updated_at_when_model_updated_then_updated_at_is_updated(
        self, async_session: AsyncSession
    ) -> None:
        dummy = DummyModel(id="dummy_id3")
        async_session.add(dummy)

        await async_session.commit()

        original_updated_at = dummy.updated_at

        # Wait to ensure timestamp changes
        time.sleep(0.1)
        dummy.id = "dummy_id3"  # simulate an update, you can also add an actual
        # property to change
        await async_session.commit()

        # Refresh from db
        await async_session.refresh(dummy)
        assert ensure_utc(dummy.updated_at) > ensure_utc(original_updated_at)
