from uuid import uuid4

from building_blocks.domain.aggregate_root import AggregateRoot
from building_blocks.domain.messages.event import Event


class DummyEvent(Event):
    @property
    def event_type(self) -> str:
        return "DummyEvent"

    @property
    def payload(self) -> dict:
        return {}


class FakeAggregateRoot(AggregateRoot):
    pass


class TestAggregateRoot:
    def test_increment_version_when_called_then_increment_version(self) -> None:
        initial_version = 0
        agg = FakeAggregateRoot(uuid4(), version=initial_version)

        agg._increment_version()

        assert agg.version == initial_version + 1

    def test_mark_changes_as_committed_when_called_then_clear_uncommitted_events(
        self,
    ) -> None:
        version = 3
        agg = FakeAggregateRoot(uuid4(), version=version)

        agg.mark_changes_as_committed()

        expected_version = version + 1
        assert agg.version == expected_version

    def test_mark_changes_as_committed_when_called_then_increment_version(self) -> None:
        version = 1
        agg = FakeAggregateRoot(uuid4(), version=version)

        agg.mark_changes_as_committed()

        expected_version = version + 1
        assert agg.version == expected_version

    def test_record_event_when_called_then_append_event(self) -> None:
        event = DummyEvent()
        agg = FakeAggregateRoot(uuid4())

        agg.record_event(event)

        assert agg.uncommitted_changes() == [event]

    def test_uncommitted_changes_called_then_list_of_events(self) -> None:
        e = DummyEvent()
        agg = FakeAggregateRoot(uuid4())
        agg._uncommitted_events.append(e)

        agg.uncommitted_changes()

        assert len(agg.uncommitted_changes()) == 1

    def test_init_with_negative_version(self) -> None:
        agg = FakeAggregateRoot(uuid4(), version=-1)
        assert agg.version == -1
        agg.mark_changes_as_committed()
        assert agg.version == 0
