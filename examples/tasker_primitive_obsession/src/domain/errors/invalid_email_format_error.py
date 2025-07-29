from building_blocks.domain.domain_error import DomainError


class InvalidEmailFormatError(DomainError):
    """Exception raised for errors in the input email format."""

    def __init__(self, message: str = "Invalid email format."):
        super().__init__(message)
