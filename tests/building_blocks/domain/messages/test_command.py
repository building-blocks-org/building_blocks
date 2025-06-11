"""
Unit tests for the Command module.

Tests for Command class.
"""

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from building_blocks.domain.messages.command import Command
from building_blocks.domain.messages.message import Message, MessageMetadata


class FakeCommand(Command):
    """A fake command for testing the Command class."""

    def __init__(
        self,
        customer_id: str,
        amount: float,
        metadata: Optional[MessageMetadata] = None,
    ):
        super().__init__(metadata)
        self._customer_id = customer_id
        self._amount = amount

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def payload(self) -> dict[str, Any]:
        return {"customer_id": self._customer_id, "amount": self._amount}


class TestCommand:
    """Tests for Command class."""

    def test_inheritance_when_created_then_is_message(self):
        command = FakeCommand("customer_123", 99.99)

        assert isinstance(command, Message)
        assert isinstance(command, Command)

    def test_convenience_properties_when_called_then_delegates_to_message(self):
        custom_metadata = MessageMetadata(
            message_id=uuid4(),
            created_at=datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc),
        )

        command = FakeCommand("customer_123", 99.99, metadata=custom_metadata)

        assert command.command_id == command.message_id
        assert command.issued_at == command.created_at
        assert command.command_id == custom_metadata.message_id
        assert command.issued_at == custom_metadata.created_at

    def test_message_type_when_called_then_returns_command_class_name(self):
        command = FakeCommand("customer_123", 99.99)

        assert command.message_type == "FakeCommand"

    def test_to_dict_when_called_then_includes_command_payload(self):
        message_id = uuid4()
        created_at = datetime(2025, 6, 11, 19, 36, 6, tzinfo=timezone.utc)
        metadata = MessageMetadata(message_id=message_id, created_at=created_at)

        command = FakeCommand("customer_123", 99.99, metadata=metadata)
        result = command.to_dict()

        expected = {
            "message_id": str(message_id),
            "created_at": "2025-06-11T19:36:06+00:00",
            "message_type": "FakeCommand",
            "customer_id": "customer_123",
            "amount": 99.99,
        }
        assert result == expected

    def test_payload_when_called_then_returns_command_data(self):
        command = FakeCommand("customer_123", 99.99)
        payload = command.payload

        expected = {"customer_id": "customer_123", "amount": 99.99}
        assert payload == expected

    def test_equality_when_same_command_id_then_true(self):
        metadata = MessageMetadata()

        command1 = FakeCommand("customer_123", 99.99, metadata=metadata)
        command2 = FakeCommand(
            "customer_456", 199.99, metadata=metadata
        )  # Different data, same metadata

        assert command1 == command2  # Commands are equal by command_id, not domain data

    def test_domain_semantics_when_command_created_then_uses_imperative_naming(self):
        # This is more of a documentation test - commands should be named in imperative
        # mood
        command = FakeCommand("customer_123", 99.99)

        # The class name should suggest an action to perform
        # This test documents the expected naming convention
        assert "Command" in command.__class__.__name__
        assert hasattr(command, "issued_at")  # Commands have issued_at, not occurred_at
        assert hasattr(command, "command_id")  # Commands have command_id, not event_id
