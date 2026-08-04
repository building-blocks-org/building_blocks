"""Concrete validation failure error for throwing at input validation sites.

Defines ``ValidationFailedError``, the concrete throwable leaf class
for validation failures. ``ValidationError`` is the abstract base;
code that constructs and raises a validation error MUST use
``ValidationFailedError``. It extends ``ValidationError`` (which extends
``ValueErrorMixin`` and ``Error[object]``).
"""

from forging_blocks.foundation.errors.base.validation_error import ValidationError


class ValidationFailedError(ValidationError):
    """A concrete validation failure that can be thrown when input validation fails.

    This is the concrete leaf class for validation errors. ``ValidationError``
    is the abstract base; code that constructs and raises a validation error
    MUST use ``ValidationFailedError``.

    Example:
        ```python
        from forging_blocks.foundation.errors import ErrorMessage

        err = ValidationFailedError(ErrorMessage("Email is required"))
        assert isinstance(err, ValueError)
        raise err
        ```
    """
