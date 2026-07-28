"""Module defining validation errors associated with a specific field.

Defines ValidationFieldErrors which represents validation errors
associated with a single field.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.combined.field_errors import FieldErrors


class ValidationFieldErrors(FieldErrors[Error[object]]):
    """Validation errors associated with a specific field."""

    ...
