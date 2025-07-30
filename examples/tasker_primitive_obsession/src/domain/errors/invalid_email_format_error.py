from building_blocks.domain.errors import DomainValidationError


class InvalidEmailFormatError(DomainValidationError):
    """Exception raised for errors in the input email format."""

    def __init__(self, message: str = "Invalid email format."):
        super().__init__(message)
