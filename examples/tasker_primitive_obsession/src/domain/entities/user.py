from __future__ import annotations

from uuid import UUID

from building_blocks.domain.aggregate_root import AggregateRoot


class User(AggregateRoot[UUID]):
    """
    Represents a user in the domain model.
    This class extends AggregateRoot to provide a unique identifier and versioning
    for optimistic concurrency control.
    Args:
        user_id (UUID): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email address of the user.
        password (str): Password for the user account.
        role (str): Role of the user, default is "user".
        version (int): Version number for optimistic concurrency control.
    """

    USER_ROLE_ENGINEER = "engineer"
    USER_ROLE_DESIGNER = "designer"
    USER_ROLE_MANAGER = "manager"

    def __init__(
        self,
        user_id: UUID,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: int = 0,
    ) -> None:
        super().__init__(user_id, version)
        self._name = name
        self._email = email
        self._password = password
        self._role = role

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @property
    def role(self) -> str:
        return self._role

    def change_role(self, new_role: str) -> None:
        valid_roles = [
            self.USER_ROLE_ENGINEER,
            self.USER_ROLE_DESIGNER,
            self.USER_ROLE_MANAGER,
        ]
        if new_role not in valid_roles:
            raise ValueError(
                f"Invalid role: {new_role}. Valid roles are: {valid_roles}"
            )
        self._role = new_role

    def __str__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"role={self.role}, "
            f"version={self.version})"
        )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, "
            f"name={self.name}, "
            f"email={self.email}, "
            f"role={self.role}, "
            f"version={self.version})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
