"""Collection of validation errors scoped to a single field.

Defines ``ValidationFieldErrors``, which aggregates multiple
``Error[MetadataValueType]`` instances for one field, enabling per-field
error reporting in validation workflows. Extends ``ValueErrorMixin``
(catchable as ``ValueError``) and ``FieldErrors[Error[MetadataValueType]]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.combined.field_errors import FieldErrors
from forging_blocks.foundation.errors.core import MetadataValueType


class ValidationFieldErrors(ValueErrorMixin, FieldErrors[Error[MetadataValueType]]):
    """Validation errors associated with a specific field."""
