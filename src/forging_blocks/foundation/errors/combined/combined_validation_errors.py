"""Aggregate error that collects multiple ``ValidationFieldErrors`` instances.

Defines ``CombinedValidationErrors``, used when input validation produces
errors across multiple fields and all failures should be reported together
in a single error response.

Extends ``ValueErrorMixin`` (catchable as ``ValueError``) and
``CombinedErrors[ValidationFieldErrors]``.
"""

from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.combined.combined_errors import CombinedErrors
from forging_blocks.foundation.errors.combined.validation_field_errors import ValidationFieldErrors


class CombinedValidationErrors(ValueErrorMixin, CombinedErrors[ValidationFieldErrors]):
    """Aggregates multiple validation errors for easier handling and reporting.

    Example:
        ```python
        from forging_blocks.foundation.errors import (
            CombinedValidationErrors,
            ErrorMessage,
            FieldReference,
            ValidationFieldErrors,
        )
        from forging_blocks.foundation.errors import Error as FBError

        fe1 = ValidationFieldErrors(
            FieldReference("username"), [FBError[str](ErrorMessage("Too short"))]
        )
        fe2 = ValidationFieldErrors(
            FieldReference("email"), [FBError[str](ErrorMessage("Invalid format"))]
        )
        combined = CombinedValidationErrors([fe1, fe2])
        assert isinstance(combined, ValueError)
        print(len(combined))  # 2
        ```
    """
