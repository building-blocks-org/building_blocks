from building_blocks.domain.errors import DomainValidationError


class InvalidTagError(DomainValidationError):
    """
    Exception raised when a tag is invalid.

    This error is used to indicate that a tag does not meet the required
    criteria for validity, such as being empty or exceeding length limits.
    """

    def __init__(self, message: str = "Tag is invalid.") -> None:
        super().__init__(message)
