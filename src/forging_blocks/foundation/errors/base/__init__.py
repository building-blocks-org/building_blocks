"""Base error contracts — abstract classes for subclassing and isinstance checks."""

from .error import Error
from .rule_violation_error import RuleViolationError
from .validation_error import ValidationError

__all__ = ["Error", "RuleViolationError", "ValidationError"]
