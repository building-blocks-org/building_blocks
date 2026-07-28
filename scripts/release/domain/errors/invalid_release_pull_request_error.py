from forging_blocks.foundation import ErrorMessage, ValidationFailedError


class InvalidReleasePullRequestError(ValidationFailedError):
    def __init__(self, reason: str) -> None:
        super().__init__(ErrorMessage(reason))
