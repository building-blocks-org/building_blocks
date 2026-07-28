from forging_blocks.foundation.errors.core import ErrorMessage
from forging_blocks.foundation.errors.rule_violations.rule_violated_error import RuleViolatedError


class ChangelogGenerationError(RuleViolatedError):
    """Raised when changelog generation fails."""

    def __init__(self, details: str) -> None:
        message = ErrorMessage(f"Changelog generation failed: {details}")
        super().__init__(message)
