from datetime import datetime

from taskflow_primitive_obsession.domain.entities.task import Task


class TestTask:
    def test_mark_as_done_when_called_then_ser_attribute_as_coompleted(self):
        task = Task(
            id_="123",
            name="Test Task",
            description="This is a test task",
            priority="high",
            due_date=datetime(2023, 10, 1),
            status="pending",
        )

        task.mark_as_done()

        expected_status = "completed"
        assert task.status is expected_status, (
            f"Expected task status to be '{expected_status}', "
            f"but got '{task.status}'"
        )
