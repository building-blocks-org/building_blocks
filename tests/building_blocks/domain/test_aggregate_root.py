"""
Unit tests for the AggregateRoot module.

Tests for AggregateRoot class using Vaughn Vernon's approach.
"""

from typing import Any, Optional
from uuid import UUID, uuid4

from building_blocks.domain.aggregate_root import AggregateRoot
from building_blocks.domain.entity import Entity
from building_blocks.domain.messages.event import Event
from building_blocks.domain.messages.message import MessageMetadata


class FakeEvent(Event):
    """A fake event for testing."""

    def __init__(self, data: str, metadata: Optional[MessageMetadata] = None):
        super().__init__(metadata)
        self._data = data

    @property
    def data(self) -> str:
        return self._data

    @property
    def payload(self) -> dict[str, Any]:
        return {"data": self._data}


class FakeAggregateRoot(AggregateRoot[UUID]):
    """A fake aggregate root for testing."""

    def __init__(self, aggregate_id: UUID, name: str, version: int = 0):
        super().__init__(aggregate_id, version)
        self._name = name
        self._actions: list[str] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def actions(self) -> list[str]:
        return self._actions.copy()

    def perform_action(self, action: str) -> None:
        """Perform an action that records a domain event."""
        self._actions.append(action)

        # Record a domain event using Vernon's approach
        event = FakeEvent(f"Action performed: {action}")
        self.record_event(event)

    def change_name(self, new_name: str) -> None:
        """Change the name and increment version."""
        old_name = self._name
        self._name = new_name
        self._increment_version()

        # Record a domain event using Vernon's approach
        event = FakeEvent(f"Name changed from {old_name} to {new_name}")
        self.record_event(event)

    def perform_business_operation(self) -> None:
        """A business operation that records multiple events."""
        self.record_event(FakeEvent("Operation started"))
        self.record_event(FakeEvent("Operation in progress"))
        self.record_event(FakeEvent("Operation completed"))


class TestAggregateRoot:
    """Tests for AggregateRoot class using Vernon's approach."""

    def test_inheritance_when_created_then_is_entity(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        assert isinstance(aggregate, Entity)
        assert isinstance(aggregate, AggregateRoot)
        assert aggregate.id == aggregate_id

    def test_generic_typing_when_created_then_preserves_id_type(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        # The aggregate should maintain the UUID type
        assert isinstance(aggregate.id, UUID)
        assert aggregate.id == aggregate_id

    def test_init_when_no_version_then_starts_at_zero(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        assert aggregate.version == 0
        assert aggregate.uncommitted_changes() == []

    def test_init_when_custom_version_then_uses_provided_version(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test", version=5)

        assert aggregate.version == 5
        assert aggregate.uncommitted_changes() == []

    def test_record_event_when_called_then_event_recorded(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("test_action")

        changes = aggregate.uncommitted_changes()
        assert len(changes) == 1
        assert isinstance(changes[0], FakeEvent)
        fake_event = changes[0]  # Type narrowing for mypy
        assert isinstance(fake_event, FakeEvent)
        assert fake_event.data == "Action performed: test_action"

    def test_uncommitted_changes_when_called_then_returns_copy(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("test_action")

        changes1 = aggregate.uncommitted_changes()
        changes2 = aggregate.uncommitted_changes()

        # Should be different objects (copies)
        assert changes1 is not changes2
        # But with same content
        assert changes1 == changes2

        # Modifying returned list shouldn't affect aggregate
        changes1.clear()
        assert len(aggregate.uncommitted_changes()) == 1

    def test_mark_changes_as_committed_clears_events_and_increments_version(
        self,
    ):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test", version=3)

        # Record some events
        aggregate.perform_business_operation()  # Records 3 events
        assert len(aggregate.uncommitted_changes()) == 3
        assert aggregate.version == 3

        # Mark as committed
        aggregate.mark_changes_as_committed()

        # Events should be cleared and version incremented
        assert len(aggregate.uncommitted_changes()) == 0
        assert aggregate.version == 4

    def test_multiple_operations_when_performed_then_events_accumulate(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("action1")
        aggregate.perform_action("action2")
        aggregate.change_name("new_name")

        changes = aggregate.uncommitted_changes()
        assert len(changes) == 3

        # Type narrowing for mypy
        fake_events = [change for change in changes if isinstance(change, FakeEvent)]
        assert len(fake_events) == 3
        assert fake_events[0].data == "Action performed: action1"
        assert fake_events[1].data == "Action performed: action2"
        assert fake_events[2].data == "Name changed from test to new_name"

    def test_version_control_scenario_tracks_version_correctly(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        initial_version = aggregate.version
        assert initial_version == 0

        # First change
        aggregate.change_name("name1")
        assert aggregate.version == 1

        # Second change
        aggregate.change_name("name2")
        assert aggregate.version == 2

        # Commit changes (simulating persistence)
        aggregate.mark_changes_as_committed()
        assert aggregate.version == 3
        assert len(aggregate.uncommitted_changes()) == 0

        # Another change after commit
        aggregate.change_name("name3")
        assert aggregate.version == 4
        assert len(aggregate.uncommitted_changes()) == 1

    def test_equality_when_same_id_then_equal_regardless_of_version(self):
        aggregate_id = uuid4()

        aggregate1 = FakeAggregateRoot(aggregate_id, "test1", version=1)
        aggregate2 = FakeAggregateRoot(aggregate_id, "test2", version=5)

        # Should be equal because Entity equality is based on ID
        assert aggregate1 == aggregate2
        assert hash(aggregate1) == hash(aggregate2)

    def test_equality_when_different_id_then_not_equal(self):
        aggregate1 = FakeAggregateRoot(uuid4(), "test", version=1)
        aggregate2 = FakeAggregateRoot(uuid4(), "test", version=1)

        assert aggregate1 != aggregate2
        assert hash(aggregate1) != hash(aggregate2)

    def test_vernon_naming_convention_integration_full_cycle_works(self):
        """Integration test using Vernon's naming conventions."""
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "order")

        # 1. Perform business operations (record events)
        aggregate.perform_action("create")
        aggregate.perform_action("validate")
        aggregate.change_name("validated_order")

        # 2. Check uncommitted changes were recorded
        changes = aggregate.uncommitted_changes()
        assert len(changes) == 3
        assert aggregate.version == 1  # Only change_name increments version

        # 3. Simulate publishing events (get copy before committing)
        events_to_publish = aggregate.uncommitted_changes()
        assert len(events_to_publish) == 3

        # 4. Mark changes as committed after successful publishing and persistence
        aggregate.mark_changes_as_committed()
        assert aggregate.version == 2
        assert len(aggregate.uncommitted_changes()) == 0

        # 5. Continue with more operations
        aggregate.perform_action("ship")
        assert len(aggregate.uncommitted_changes()) == 1
        assert aggregate.version == 2  # Version only incremented on commit


class TestDomainEventManagement:
    """Tests focused on domain event management using Vernon's approach."""

    def test_event_ordering_when_multiple_events_then_preserves_order(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        # Events should be recorded in order
        aggregate.perform_action("first")
        aggregate.perform_action("second")
        aggregate.perform_action("third")

        changes = aggregate.uncommitted_changes()
        fake_events = [change for change in changes if isinstance(change, FakeEvent)]
        assert fake_events[0].data == "Action performed: first"
        assert fake_events[1].data == "Action performed: second"
        assert fake_events[2].data == "Action performed: third"

    def test_event_immutability_cannot_modify_internally(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("test")

        # Get uncommitted changes
        changes = aggregate.uncommitted_changes()
        original_count = len(changes)

        # Try to modify returned list (should not affect aggregate)
        changes.append(FakeEvent("malicious_event"))
        changes.clear()

        # Aggregate's events should be unchanged
        assert len(aggregate.uncommitted_changes()) == original_count
        fake_event = aggregate.uncommitted_changes()[0]
        assert isinstance(fake_event, FakeEvent)
        assert fake_event.data == "Action performed: test"

    def test_event_metadata_when_event_recorded_then_has_proper_metadata(self):
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        aggregate.perform_action("test")

        event = aggregate.uncommitted_changes()[0]
        assert event.event_id is not None
        assert event.occurred_at is not None
        assert event.message_type == "FakeEvent"

    def test_vernon_approach_method_names_follows_conventions(self):
        """Test that we're following Vernon's naming conventions."""
        aggregate_id = uuid4()
        aggregate = FakeAggregateRoot(aggregate_id, "test")

        # Vernon's method names should be available
        assert hasattr(aggregate, "record_event")
        assert hasattr(aggregate, "uncommitted_changes")
        assert hasattr(aggregate, "mark_changes_as_committed")

        # Use Vernon's approach
        aggregate.record_event(FakeEvent("direct_event"))
        changes = aggregate.uncommitted_changes()
        assert len(changes) == 1

        aggregate.mark_changes_as_committed()
        assert len(aggregate.uncommitted_changes()) == 0
