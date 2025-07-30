from __future__ import annotations

import re
from collections import defaultdict
from typing import List, Optional
from uuid import UUID, uuid4

from examples.tasker_primitive_obsession.src.domain.errors import ChangeUserRoleError

from building_blocks.abstractions.result import Err, Ok, Result
from building_blocks.domain.aggregate_root import AggregateRoot, AggregateVersion
from building_blocks.domain.errors import DomainValidationError


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
        version (Optional[AggregateVersion]): Version number for optimistic concurrency
        control.
    """

    _valid_roles = [
        "admin",
        "engineer",
        "designer",
        "manager",
    ]

    def __init__(
        self,
        user_id: UUID,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: Optional[AggregateVersion] = None,
    ) -> None:
        super().__init__(user_id, version)
        self._name = name
        self._email = email
        self._password = password
        self._role = role

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

    @classmethod
    def create(
        cls,
        user_id: UUID,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: Optional[AggregateVersion] = None,
    ) -> Result[User, DomainValidationError]:
        errors = defaultdict(list)

        user_id_result = cls._validate_user_id(user_id)
        if isinstance(user_id_result, Err):
            errors["user_id"].extend(user_id_result.error)

        name_result = cls._validate_name(name)
        if isinstance(name_result, Err):
            errors["name"].extend(name_result.error)

        email_result = cls._validate_email(email)
        if isinstance(email_result, Err):
            errors["email"].extend(email_result.error)

        password_result = cls._validate_password(password)
        if isinstance(password_result, Err):
            errors["password"].extend(password_result.error)

        role_result = cls._validate_role(role)
        if isinstance(role_result, Err):
            errors["role"].extend(role_result.error)

        if errors:
            return Err(
                DomainValidationError(
                    "User creation failed due to validation errors.",
                    context=dict(errors),
                )
            )

        user = cls(user_id, name, email, password, role, version)

        return Ok(user)

    @classmethod
    def register(
        cls,
        name: str,
        email: str,
        password: str,
        role: str = "engineer",
        version: Optional[AggregateVersion] = None,
    ) -> Result[User, DomainValidationError]:
        user_id = uuid4()

        return cls.create(user_id, name, email, password, role, version)

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_password: str) -> None:
        password_result = self._validate_password(new_password)
        if isinstance(password_result, Err):
            raise DomainValidationError(
                "Password validation failed.",
                context={"password": password_result.error},
            )
        self._password = new_password

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, new_role: str) -> None:
        role_result = self._validate_role(new_role)
        if isinstance(role_result, Err):
            raise DomainValidationError(
                "Role validation failed.",
                context={"role": role_result.error},
            )

        if new_role == self._role:
            raise ChangeUserRoleError(f"User already has the role '{new_role}'.")

        self._role = new_role

    @classmethod
    def _validate_user_id(cls, user_id: UUID) -> Result[UUID, List[str]]:
        errors = []

        if not user_id:
            errors.append("User ID cannot be empty.")

        if errors:
            return Err(errors)

        return Ok(user_id)

    @classmethod
    def _validate_name(cls, name: str) -> Result[str, List[str]]:
        errors = []

        if not name or not name.strip():
            errors.append("cannot be empty.")
        if len(name) < 3:
            errors.append("must be at least 3 characters long.")
        if not all(char.isalpha() or char.isspace() for char in name):
            errors.append("must contain only alphabetic characters.")

        if errors:
            return Err(errors)

        return Ok(name)

    @classmethod
    def _validate_email(
        cls,
        email: str,
    ) -> Result[str, List[str]]:
        errors = []

        if not email or not email.strip():
            errors.append("cannot be empty.")
        if "@" not in email or "." not in email.split("@")[-1]:
            errors.append("must be a valid email format.")

        if errors:
            return Err(errors)

        return Ok(email)

    @classmethod
    def _validate_password(
        cls,
        password: str,
    ) -> Result[str, List[str]]:
        errors = []

        if not password or not password.strip():
            errors.append("cannot be empty.")
        if re.search(r"\s", password):
            errors.append("must not contain whitespace.")
        if len(password) < 8:
            errors.append("must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            errors.append("must contain at least one digit.")
        if not any(char.islower() for char in password) or not any(
            char.isupper() for char in password
        ):
            errors.append("must contain both uppercase and lowercase letters.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=~`[\]\\;/']", password):
            errors.append("must contain at least one special character.")

        if errors:
            return Err(errors)

        return Ok(password)

    @classmethod
    def _validate_role(cls, role: str) -> Result[str, List[str]]:
        errors = []

        if role not in cls._valid_roles:
            errors.append(f"Invalid role: {role}. Valid roles are: {cls._valid_roles}")

        if errors:
            return Err(errors)
        return Ok(role)
