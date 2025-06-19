from unittest import mock

from taskflow_primitives.domain.entities.task import Task


class TestTask:
    def test_constructor_when_no_tags_then_tags_is_empty_list(self):
        id_ = "1234567890abcdef"

        task = Task(
            id_=id_,
            title="Test Task",
            description="This is a test task.",
            due_date="2023-10-01",
            priority=1,
        )
        assert task.tags == []

    def test_constructor_when_all_attributes_then_all_attributes_are_set(self):
        id_ = "1234567890abcdef"

        task = Task(
            id_=id_,
            title="Test Task",
            description="This is a test task.",
            due_date="2023-10-01",
            priority=1,
            status="pending",
            tags=["urgent", "work"],
        )

        assert task.title == "Test Task"
        assert task.description == "This is a test task."
        assert task.due_date == "2023-10-01"
        assert task.priority == 1
        assert task.status == "pending"
        assert task.tags == ["urgent", "work"]

    @mock.patch("taskflow_primitives.domain.entities.task.uuid4")
    def test_create_pending_when_no_tags_then_tags_is_empty_list(
        self, uuid4_mock: mock.Mock
    ):
        uuid4_mock.return_value.hex = "1234567890abcdef"
        task = Task.create_pending(
            title="Test Task",
            description="This is a test task.",
            due_date="2023-10-01",
            priority=1,
        )
        assert task.tags == []

    def test_create_pending_when_all_attributes_then_all_attributes_are_set(self):
        task = Task.create_pending(
            title="Test Task",
            description="This is a test task.",
            due_date="2023-10-01",
            priority=1,
            tags=["urgent", "work"],
        )
        assert task.title == "Test Task"
        assert task.description == "This is a test task."
        assert task.due_date == "2023-10-01"
        assert task.priority == 1
        assert task.status == "pending"
        assert task.tags == ["urgent", "work"]

    def test_mark_completed_changes_status_to_completed(self):
        task = Task.create_pending(
            title="Test Task",
            description="This is a test task.",
            due_date="2023-10-01",
            priority=1,
        )
        task.mark_completed()
        assert task.status == "completed"
