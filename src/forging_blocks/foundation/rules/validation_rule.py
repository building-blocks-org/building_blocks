"""Abstract base class for a synchronous validation rule."""

from abc import ABC, abstractmethod
from typing import Any

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError


class ValidationRule(ABC):
    """Abstract base class for a synchronous validation rule.

    Example:
        ```python
        from forging_blocks.foundation.rules import ValidationRule


        class RuleViolationError(Exception):
            def __init__(self, message: str) -> None:
                super().__init__(message)


        class ErrorMessage:
            def __init__(self, text: str) -> None:
                self.text = text


        class MaxLengthRule(ValidationRule):
            def __init__(self, max_len: int) -> None:
                self.max_len = max_len

            def validate(self, value: object) -> list[RuleViolationError]:
                if isinstance(value, str) and len(value) > self.max_len:
                    return [RuleViolationError(ErrorMessage(f"Too long (max {self.max_len})"))]
                return []


        rule = MaxLengthRule(10)
        assert len(rule.validate("short")) == 0
        assert len(rule.validate("this is way too long")) == 1
        ```
    """

    @abstractmethod
    def validate(self, value: Any) -> list[RuleViolationError]:
        """Validate *value* and return any errors found."""
