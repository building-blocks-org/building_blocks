"""Module defining combined rule violation errors.

Defines CombinedRuleViolationErrors which aggregates multiple
RuleViolationError instances into a single error.
"""

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.combined.combined_errors import CombinedErrors


class CombinedRuleViolationErrors(RuntimeErrorMixin, CombinedErrors[RuleViolationError]):
    """Aggregates multiple rule violation errors for easier handling and reporting."""
