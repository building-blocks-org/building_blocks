from building_blocks.domain.domain_error import DomainError


class InvalidTagError(DomainError):
    """
    Exception raised when a tag is invalid.

    This error is used to indicate that a tag does not meet the required
    criteria for validity, such as being empty or exceeding length limits.
    """

    def __init__(self, message: str = "Tag must be a non-empty string") -> None:
        super().__init__(message)
