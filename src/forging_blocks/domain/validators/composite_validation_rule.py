"""Combines multiple validation rules into a single rule."""

from typing import Any

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.rules import ValidationRule


class CompositeValidationRule(ValidationRule):
    """Combines multiple ``ValidationRule`` instances into a single rule.

    All rules are evaluated and their errors are concatenated (no
    short-circuit), so every validation failure is reported.

    Example:
        ```python
        composite = CompositeValidationRule(
            [
                RequiredValidator("username"),
                LengthValidator("username", minimum_length=3, maximum_length=20),
            ]
        )

        errors = composite.validate("")
        assert len(errors) == 2  # fails both required and minimum length

        errors = composite.validate("alice")
        assert errors == []
        ```
    """

    def __init__(self, rules: list[ValidationRule]) -> None:
        self._rules = rules

    def validate(self, value: Any) -> list[RuleViolationError]:
        errors: list[RuleViolationError] = []
        for rule in self._rules:
            errors.extend(rule.validate(value))
        return errors
