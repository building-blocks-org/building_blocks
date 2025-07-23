from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from examples.tasker_primitives.src.application.ports import (
    AuthenticateUserUseCase,
    RegisterUserUseCase,
)
from examples.tasker_primitives.src.application.services.authenticate_user_service import (
    AuthenticateUserService,
)
from examples.tasker_primitives.src.application.services.register_user_service import (
    RegisterUserService,
)
from examples.tasker_primitives.src.infrastructure.hashing.bcrypt import (
    BCryptPasswordHasher,
    BCryptPasswordVerifier,
)
from examples.tasker_primitives.src.infrastructure.persistence.repositories import (
    SQLAlchemyUserRepository,
)
from examples.tasker_primitives.src.infrastructure.token.jwt_token_generators import (
    jwt_access_token_generator,
    jwt_refresh_token_generator,
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


async def get_authenticate_user_use_case(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository),
) -> AuthenticateUserUseCase:
    password_verifier = BCryptPasswordVerifier()

    return AuthenticateUserService(
        repo,
        password_verifier,
        jwt_access_token_generator,
        jwt_refresh_token_generator,
    )
