"""Module defining combined validation errors.

Defines CombinedValidationErrors which aggregates multiple
ValidationFieldErrors instances into a single error.
"""

from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.combined.combined_errors import CombinedErrors
from forging_blocks.foundation.errors.combined.validation_field_errors import ValidationFieldErrors


class CombinedValidationErrors(ValueErrorMixin, CombinedErrors[ValidationFieldErrors]):
    """Aggregates multiple validation errors for easier handling and reporting."""
