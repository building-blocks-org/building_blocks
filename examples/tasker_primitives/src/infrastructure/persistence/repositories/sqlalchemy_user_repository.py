from typing import Any, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from examples.tasker_primitives.src.domain.entities.user import User
from examples.tasker_primitives.src.domain.ports import UserRepository
from examples.tasker_primitives.src.infrastructure.persistence.helpers import (
    build_upsert_statement,
)
from examples.tasker_primitives.src.infrastructure.persistence.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        values = self._build_values(user)

        dialect_name = self._session.bind.dialect.name

        upsert_statement = build_upsert_statement(
            dialect_name, UserModel.__table__, values
        )

        await self._session.execute(upsert_statement)
        await self._session.commit()

    async def find_all(self) -> List[User]:
        statement = select(UserModel)
        result = await self._session.execute(statement)
        models = result.scalars().all()

        return [model.to_entity() for model in models]

    async def find_by_id(self, user_id: str) -> Optional[User]:
        model = await self._session.get(UserModel, user_id)

        if model:
            return model.to_entity()
        return None

    async def delete(self, user: User) -> None:
        model = await self._session.get(UserModel, user.id)

        if model:
            await self._session.delete(model)
            await self._session.commit()

    async def find_by_email(self, email: str) -> Optional[User]:
        statement = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(statement)
        model = result.scalars().first()

        if model:
            return model.to_entity()
        return None

    def _build_values(self, user: User) -> dict[str, Any]:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "role": user.role,
            "version": user.version,
        }
