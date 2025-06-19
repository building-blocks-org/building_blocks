from datetime import date

from taskflow_primitives.domain.entities.task import Task
from taskflow_primitives.infrastructure.persistence.models.sqlalchemy_task import (
    SQLAlchemyTask,
)


class TestSQLAlchemyTaskModel:
    def test_from_entity(self):
        task = Task.create_pending(
            title="Test Task",
            description="This is a test task.",
            due_date=date(2023, 10, 1),
            priority=1,
            tags=["urgent", "work"],
        )

        model = SQLAlchemyTask.from_entity(task)

        assert model.id_ == task._id
        assert model.title == task.title
        assert model.description == task.description
        assert model.due_date == task.due_date
        assert model.priority == task.priority
        assert model.status == task.status
        assert model.tags == task.tags

    def test_to_entity(self):
        model = SQLAlchemyTask(
            id_="1234567890abcdef",
            title="Test Task",
            description="This is a test task.",
            due_date=date(2023, 10, 1),
            priority=1,
            status="pending",
            tags=["urgent", "work"],
        )

        entity = model.to_entity()

        assert entity._id == model.id_
        assert entity.title == model.title
        assert entity.description == model.description
        assert entity.due_date == model.due_date
        assert entity.priority == model.priority
        assert entity.status == model.status
        assert entity.tags == model.tags
