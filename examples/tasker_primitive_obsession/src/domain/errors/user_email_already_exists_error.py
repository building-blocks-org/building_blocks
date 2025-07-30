from typing import Optional

from building_blocks.domain.errors import DomainRuleViolationError


class UserEmailAlreadyExistsError(DomainRuleViolationError):
    """Exception raised when a user with the same email already exists."""

    def __init__(self, email: str, message: Optional[str] = None):
        self.email = email
        error_message = message or f"User with email '{email}' already exists."
        context = {"email": email}
        super().__init__(error_message, context=context)

    def __str__(self):
        return f"UserEmailAlreadyExistsError: {self.email}"
