"""
Message module for domain messaging patterns.

This module provides the base Message class and MessageMetadata for implementing
domain messages following Domain-Driven Design (DDD) and CQRS principles.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock, patch

from building_blocks.domain.messages.event import Event


class FakeEvent(Event):
    @property
    def payload(self) -> dict[str, Any]:
        return {"data": "test"}


class TestEvent:
    @patch("building_blocks.domain.messages.message.uuid4")
    def test_event_id(self, mock_uuid: Mock) -> None:
        actual_event_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_uuid.return_value = actual_event_id

        event = FakeEvent()

        assert event.event_id == actual_event_id

    def test_payload(self) -> None:
        event = FakeEvent()
        assert event.payload == {"data": "test"}
