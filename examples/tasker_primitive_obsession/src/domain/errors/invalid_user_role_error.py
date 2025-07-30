from building_blocks.domain.errors import DomainValidationError


class InvalidRoleError(DomainValidationError):
    """
    Exception raised when a user role is invalid.

    This error is used to indicate that a user role does not meet the required
    criteria for validity, such as being empty or not matching predefined roles.
    """

    def __init__(self, message: str = "User role is invalid.") -> None:
        super().__init__(message)
