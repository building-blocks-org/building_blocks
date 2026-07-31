"""ForgingBlocks foundation.errors package initialization."""

from .architecture_error import ArchitectureError
from .base.error import Error
from .base.rule_violation_error import RuleViolationError
from .base.validation_error import ValidationError
from .builtin import RuntimeErrorMixin, ValueErrorMixin
from .cant_modify_immutable_attribute_error import CantModifyImmutableAttributeError
from .combined.combined_errors import CombinedErrors
from .combined.combined_rule_violation_errors import CombinedRuleViolationErrors
from .combined.combined_validation_errors import CombinedValidationErrors
from .combined.field_errors import FieldErrors
from .combined.validation_field_errors import ValidationFieldErrors
from .configuration_error import ConfigurationError
from .core import ErrorMessage, ErrorMetadata, FieldReference, MetadataValueType
from .non_hashable_value_error import NonHashableValueError
from .none_not_allowed_error import NoneNotAllowedError
from .result_access_error import ResultAccessError
from .rule_violations.rule_violated_error import RuleViolatedError
from .validation.validation_failed_error import ValidationFailedError

__all__ = [
    "ArchitectureError",
    "CantModifyImmutableAttributeError",
    "CombinedErrors",
    "CombinedRuleViolationErrors",
    "CombinedValidationErrors",
    "ConfigurationError",
    "Error",
    "ErrorMessage",
    "ErrorMetadata",
    "FieldErrors",
    "FieldReference",
    "MetadataValueType",
    "NoneNotAllowedError",
    "NonHashableValueError",
    "ResultAccessError",
    "RuleViolatedError",
    "RuleViolationError",
    "RuntimeErrorMixin",
    "ValidationError",
    "ValidationFailedError",
    "ValidationFieldErrors",
    "ValueErrorMixin",
]
