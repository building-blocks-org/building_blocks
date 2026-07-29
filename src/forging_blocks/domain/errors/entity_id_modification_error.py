"""Error raised when code attempts to modify an entity's identity attribute.

Defines ``EntityIdModificationError``, raised when an attempt is made to
change an entity's identity attribute (typically ``id``) after it has already
been assigned. Once set, an entity's identity is immutable — modification
would break identity-based equality and hashing in aggregate repositories.

Extends ``RuntimeErrorMixin`` and ``Error[object]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class EntityIdModificationError(RuntimeErrorMixin, Error[object]):
    """Raised when there is an attempt to modify an entity's identifier after it has been set."""

    def __init__(self, class_name: str, attribute_name: str, current_value: object) -> None:
        """Initialise the error with the class, attribute, and current value.

        Args:
            class_name: Name of the class whose identifier was targeted.
            attribute_name: Name of the attribute that was being modified.
            current_value: The current (immutable) value of the identifier.

        """
        message = ErrorMessage(
            f"Cannot modify '{attribute_name}' of {class_name} once set "
            f"(current value={current_value!r})."
        )
        metadata = ErrorMetadata(
            {
                "class_name": class_name,
                "attribute_name": attribute_name,
                "current_value": current_value,
            }
        )
        super().__init__(message, metadata)
