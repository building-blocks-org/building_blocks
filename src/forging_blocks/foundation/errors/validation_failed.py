"""Module defining a concrete validation failure error for throwing at validation sites."""

from forging_blocks.foundation.errors.base.validation_error import ValidationError


class ValidationFailed(ValidationError):
    """A concrete validation failure that can be thrown when input validation fails.

    This is the concrete leaf class for validation errors. ``ValidationError``
    is the abstract base; code that constructs and raises a validation error
    MUST use ``ValidationFailed``.

    """
