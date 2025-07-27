from __future__ import annotations

import uuid

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from building_blocks.domain.aggregate_root import AggregateVersion
from examples.tasker_primitive_obsession.src.domain.entities.user import User

from .base import OrmModel


class UserModel(OrmModel[User, uuid.UUID]):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column("name", String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        "email", String(255), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column("password", String(255), nullable=False)
    role: Mapped[str] = mapped_column("role", String(128), nullable=False)
    version: Mapped[int] = mapped_column("version", Integer, nullable=False, default=0)

    def __init__(
        self,
        id: uuid.UUID,
        name: str,
        email: str,
        password: str,
        role: str,
        version: int = 0,
    ) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.version = version

    @classmethod
    def from_entity(cls, entity: User) -> UserModel:
        return cls(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            password=entity.password,
            role=entity.role,
            version=entity.version.value,
        )

    # --- Domain conversion ---
    def to_entity(self) -> User:
        return User(
            user_id=self.id,
            name=self.name,
            email=self.email,
            password=self.password,
            role=self.role,
            version=AggregateVersion(self.version),
        )
