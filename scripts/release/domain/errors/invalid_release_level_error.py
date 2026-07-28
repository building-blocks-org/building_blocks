from forging_blocks.foundation import ErrorMessage, ValidationFailedError


class InvalidReleaseLevelError(ValidationFailedError):
    def __init__(self, value: str) -> None:
        super().__init__(
            ErrorMessage(f"Invalid release level '{value}'. Allowed values: patch, minor, major.")
        )
