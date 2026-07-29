"""Error raised when accessing the wrong variant of a ``Result`` type.

Defines ``ResultAccessError``, raised when code accesses ``.value`` on an
``Err`` result or ``.error`` on an ``Ok`` result.  Enforces correct ``Result``
variant destructuring — callers must check ``.is_ok()`` or ``.is_err()``
before accessing the payload.

Extends ``RuntimeErrorMixin`` (catchable as ``RuntimeError``) and
``Error[object]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage


class ResultAccessError(RuntimeErrorMixin, Error[object]):
    """Exception raised when trying to access value or err from an inappropriate Result variant."""

    def __init__(self, message: ErrorMessage | None = None) -> None:
        """Initialise with an optional custom error message.

        Args:
            message: Optional `ErrorMessage` describing the invalid
                access. Defaults to a generic message when not provided.

        """
        message = message or ErrorMessage("Invalid access on Result type.")
        super().__init__(message)

    @classmethod
    def cannot_access_value(cls) -> "ResultAccessError":
        """Create an error for accessing value from an Err Result."""
        return cls(ErrorMessage("Cannot access value from an Err Result."))

    @classmethod
    def cannot_access_error(cls) -> "ResultAccessError":
        """Create an error for accessing error from an Ok Result."""
        return cls(ErrorMessage("Cannot access error from an Ok Result."))
