import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from taskflow_primitives.domain.entities.task import Task
from taskflow_primitives.infrastructure.persistence.models.sqlalchemy_task import (
    SQLAlchemyTask,
)
from taskflow_primitives.infrastructure.persistence.repositories import (
    sqlalchemy_task_repository as repo,
)


class TestSQLAlchemyTaskRepository:
    @pytest.fixture
    def task_models(self) -> list[SQLAlchemyTask]:
        return [
            SQLAlchemyTask(
                id_="1234567890abcdef",
                title="Fake Task",
                description="This is a test task.",
                due_date=datetime.date(2023, 10, 1),
                priority=1,
                status="pending",
                tags=["urgent", "fake", "work"],
            ),
            SQLAlchemyTask(
                id_="abcdef1234567890",
                title="Another Fake Task",
                description="This is a test task.",
                due_date=datetime.date(2025, 7, 19),
                priority=3,
                status="pending",
                tags=["work"],
            ),
        ]

    @pytest.fixture
    def task_repository(
        self, async_session: AsyncSession
    ) -> repo.SQLAlchemyTaskRepository:
        return repo.SQLAlchemyTaskRepository(async_session)

    @pytest.mark.asyncio
    async def test_save_when_succcess_then_add_persist_aggregate(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
    ) -> None:
        # Implement the test for saving a new task
        actual_id = "1234567890abcdef"
        task = Task(
            id_=actual_id,
            title="Test Task",
            description="This is a test task.",
            due_date=datetime.date(2023, 10, 1),
            priority=1,
            status="pending",
            tags=["urgent", "work"],
        )

        await task_repository.save(task)

        # Use a new query to the DB, not task_repository._session
        result = await async_session.execute(
            select(SQLAlchemyTask).where(SQLAlchemyTask.id_ == actual_id)
        )

        orm_task = result.scalar_one()
        assert orm_task.id_ == task._id
        assert orm_task.title == task.title
        assert orm_task.description == task.description
        assert orm_task.due_date == task.due_date
        assert orm_task.priority == task.priority
        assert orm_task.status == task.status
        assert orm_task.tags == task.tags

    @pytest.mark.asyncio
    async def test_save_when_aggregate_already_exists_then_update_existing(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
        task_models: list[SQLAlchemyTask],
    ) -> None:
        task_model = task_models[0]  # Use the first task model from the fixture

        async with async_session.begin():
            async_session.add(task_model)  # Add the existing task to the session
        await async_session.commit()  # Commit the existing task to the database

        task = Task(
            id_=task_model.id_,
            title="Updated Task",
            description="This is an updated task.",
            due_date=datetime.date(2023, 10, 2),
            priority=2,
            status="completed",
            tags=["important"],
        )

        await task_repository.save(task)

        # Use a new query to the DB, not task_repository._session
        result = await async_session.execute(
            select(SQLAlchemyTask).where(SQLAlchemyTask.id_ == task._id)
        )
        orm_task = result.scalar_one()
        assert orm_task.id_ == task._id
        assert orm_task.title == task.title
        assert orm_task.description == task.description
        assert orm_task.due_date == task.due_date
        assert orm_task.priority == task.priority
        assert orm_task.status == task.status
        assert orm_task.tags == task.tags

    @pytest.mark.asyncio
    async def test_find_by_id_when_task_exists_then_return_task(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
        task_models: list[SQLAlchemyTask],
    ) -> None:
        task_model = task_models[0]  # Use the first task model from the fixture
        aggregate_id = task_model.id_

        async with async_session.begin():
            async_session.add(task_model)  # Add the existing task to the session
        await async_session.commit()  # Commit the existing task to the database

        task = await task_repository.find_by_id(aggregate_id)

        assert task is not None
        assert task._id == aggregate_id
        assert task.title == task_model.title
        assert task.description == task_model.description
        assert task.due_date == task_model.due_date
        assert task.priority == task_model.priority
        assert task.status == task_model.status
        assert task.tags == task_model.tags

    @pytest.mark.asyncio
    async def test_find_by_id_when_task_does_not_exist_then_return_none(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
    ) -> None:
        aggregate_id = "nonexistent-id"

        task = await task_repository.find_by_id(aggregate_id)

        assert task is None

    @pytest.mark.asyncio
    async def test_find_all_when_tasks_exist_then_return_list_of_tasks(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
        task_models: list[SQLAlchemyTask],
    ) -> None:
        async with async_session.begin():
            async_session.add_all(task_models)
        await async_session.commit()

        tasks = await task_repository.find_all()

        assert len(tasks) == len(task_models)
        for index, task in enumerate(tasks):
            assert task._id == task_models[index].id_
            assert task.title == task_models[index].title
            assert task.description == task_models[index].description
            assert task.due_date == task_models[index].due_date
            assert task.priority == task_models[index].priority
            assert task.status == task_models[index].status
            assert task.tags == task_models[index].tags

    @pytest.mark.asyncio
    async def test_delete_when_task_exists_then_remove_task(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
        task_models: list[SQLAlchemyTask],
    ) -> None:
        async with async_session.begin():
            async_session.add_all(task_models)
        await async_session.commit()

        aggregate_id = task_models[0].id_

        await task_repository.delete(aggregate_id)

        # Use a new query to the DB, not task_repository._session
        result = await async_session.execute(
            select(SQLAlchemyTask).where(SQLAlchemyTask.id_ == aggregate_id)
        )
        orm_task = result.scalar_one_or_none()

        assert orm_task is None

    @pytest.mark.asyncio
    async def test_delete_when_task_does_not_exist_then_no_error(
        self,
        task_repository: repo.SQLAlchemyTaskRepository,
        async_session: AsyncSession,
    ) -> None:
        # Implement the test for deleting a task that does not exist
        aggregate_id = "nonexistent-id"
        await task_repository.delete(aggregate_id)
        # No exception should be raised, and no task should be found
        result = await async_session.execute(
            select(SQLAlchemyTask).where(SQLAlchemyTask.id_ == aggregate_id)
        )
        orm_task = result.scalar_one_or_none()
        assert orm_task is None
