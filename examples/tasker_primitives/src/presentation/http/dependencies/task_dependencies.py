from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from examples.tasker_primitives.src.application.ports import CreateTaskUseCase
from examples.tasker_primitives.src.application.services import CreateTaskService
from examples.tasker_primitives.src.infrastructure.persistence.repositories import (
    SQLAlchemyTaskRepository,
)
from examples.tasker_primitives.src.presentation.wiring import get_async_session


async def get_task_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SQLAlchemyTaskRepository:
    return SQLAlchemyTaskRepository(session)


async def get_create_task_use_case(
    repo: SQLAlchemyTaskRepository = Depends(get_task_repository),
) -> CreateTaskUseCase:
    return CreateTaskService(repo)
