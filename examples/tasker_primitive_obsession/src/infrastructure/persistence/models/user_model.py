from __future__ import annotations

import uuid

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from examples.tasker_primitive_obsession.src.domain.entities.user import User
from examples.tasker_primitive_obsession.src.infrastructure.persistence import (
    OrmModel,
)


class UserModel(OrmModel[User, uuid.UUID]):
    """
    SQLAlchemy model for User aggregate.

    This model maps the User aggregate to a database table, providing methods
    to convert between the model and the domain entity.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(128), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    def __init__(
        self, id: uuid.UUID, name: str, email: str, role: str, version: int = 0
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.role = role
        self.version = version

    def to_entity(self) -> User:
        return User(
            user_id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            role=self.role,
            version=self.version,
        )

    @classmethod
    def from_entity(cls, entity: User) -> UserModel:
        return cls(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            role=entity.role,
            version=entity.version,
        )
