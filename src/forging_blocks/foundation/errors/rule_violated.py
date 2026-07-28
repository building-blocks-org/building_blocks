"""Module defining a concrete rule violation error for throwing at violation sites."""

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError


class RuleViolated(RuleViolationError):
    """A concrete rule violation that can be thrown when a business rule is violated.

    This is the concrete leaf class for rule violations. ``RuleViolationError``
    is the abstract base; code that constructs and raises a rule violation
    MUST use ``RuleViolated``.

    """
