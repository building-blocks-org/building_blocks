from building_blocks.domain.errors import DomainValidationError


class InvalidProgressError(DomainValidationError):
    """Exception raised for errors related to invalid  progress values."""

    def __init__(self, message: str = "Invalid progress value."):
        super().__init__(message)
