from building_blocks.domain.domain_error import DomainError


class InvalidProgressError(DomainError):
    """Exception raised for errors related to invalid  progress values."""

    def __init__(self, message: str = "Invalid progress value."):
        super().__init__(message)
