"""Concrete throwable error for business rule violations.

Defines ``RuleViolatedError``, the leaf class that code MUST use when
constructing and raising a rule violation. ``RuleViolationError`` is the
abstract base class — it cannot be directly instantiated.

Extends ``RuleViolationError`` (which extends ``RuntimeErrorMixin`` and
``Error[MetadataValueType]``).
"""

from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError


class RuleViolatedError(RuleViolationError):
    """A concrete rule violation that can be thrown when a business rule is violated.

    This is the concrete leaf class for rule violations. ``RuleViolationError``
    is the abstract base; code that constructs and raises a rule violation
    MUST use ``RuleViolatedError``.

    """
