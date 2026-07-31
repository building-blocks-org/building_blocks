"""Error raised when a field value cannot be converted to a hashable equivalent.

Raised when a value is neither natively hashable nor one of the
supported convertible types (``list``, ``dict``).
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class NonHashableValueError(ValueErrorMixin, Error[str]):
    """Raised when a value cannot be made hashable during ``__hash__`` computation.

    Automatic hashability conversion supports ``list`` → ``tuple`` and
    ``dict`` → ``frozenset`` of ``(key, value)`` pairs. Values of other
    mutable types (e.g. ``bytearray``, custom objects without ``__hash__``)
    trigger this error.
    """

    def __init__(self, type_name: str, field_name: str | None = None) -> None:
        """Initialise the error with the name of the type that failed conversion.

        Args:
            type_name: The ``type(value).__name__`` of the offending value.
            field_name: Optional field name where the value was encountered.

        """
        message = ErrorMessage(
            f"Cannot convert {type_name!r} to hashable. "
            f"Use tuple, frozenset, or immutable types "
            f"in fields hashed by @auto_hash."
            + (f" Field: {field_name!r}." if field_name is not None else "")
        )
        metadata = ErrorMetadata({"type_name": type_name})
        if field_name is not None:
            metadata.context["field_name"] = field_name
        super().__init__(message, metadata)
