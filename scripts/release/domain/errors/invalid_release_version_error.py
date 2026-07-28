from forging_blocks.foundation import ErrorMessage, ErrorMetadata, ValidationFailedError


class InvalidReleaseVersionError(ValidationFailedError):
    def __init__(self, release_version: str) -> None:
        message = ErrorMessage(f"'{release_version}' should be bigger than v0.0.0")
        metadata: ErrorMetadata[str] = ErrorMetadata(context={"release_version": release_version})
        super().__init__(message, metadata)
