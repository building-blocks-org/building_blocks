from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from examples.tasker_primitives.src.application.ports import RegisterUserUseCase
from examples.tasker_primitives.src.application.services.register_user_service import (
    RegisterUserService,
)
from examples.tasker_primitives.src.infrastructure.hashing.bcrypt import (
    BCryptPasswordHasher,
)
from examples.tasker_primitives.src.infrastructure.persistence.repositories import (
    SQLAlchemyUserRepository,
)
from examples.tasker_primitives.src.presentation.wiring import get_async_session


async def get_user_repository(
    session: AsyncSession = Depends(get_async_session),
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


async def get_register_user_use_case(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> RegisterUserUseCase:
    password_hasher = BCryptPasswordHasher()

    return RegisterUserService(repo, password_hasher)
