from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.errors.core import ErrorMessage


# RuntimeError
class TagAlreadyExistsError(RuleViolationError):
    """Raised when attempting to create a release with an existing tag."""

    def __init__(self, tag_name: str) -> None:
        message = ErrorMessage(f"Tag '{tag_name}' already exists.")
        super().__init__(message)
