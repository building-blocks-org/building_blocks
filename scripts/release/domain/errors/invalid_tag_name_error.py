from forging_blocks.foundation import ErrorMessage, ValidationFailedError


class InvalidTagNameError(ValidationFailedError):
    def __init__(self, value: str) -> None:
        super().__init__(
            ErrorMessage(f"Invalid tag name '{value}'. Tags must start with 'v<version>'.")
        )
