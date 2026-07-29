"""Aggregate error for multiple simultaneous rule violations.

Defines ``CombinedRuleViolationErrors``, raised when two or more
``RuleViolationError`` instances must be reported together — for example,
when a single operation violates several business rules at once.

Extends ``RuntimeErrorMixin`` (catchable as ``RuntimeError``) and
``CombinedErrors[RuleViolationError]``, so it behaves like a standard
collection of rule violations while remaining compatible with generic
``RuntimeError`` exception handlers.
"""

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.combined.combined_errors import CombinedErrors


class CombinedRuleViolationErrors(RuntimeErrorMixin, CombinedErrors[RuleViolationError]):
    """Aggregates multiple rule violation errors for easier handling and reporting."""
