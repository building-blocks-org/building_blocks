"""Error raised when code attempts to delete an entity's identity attribute.

Defines ``EntityIdDeletionError``, raised when an entity's ``id`` field is
targeted for deletion. An entity's ``id`` defines its identity and must
never be deleted after being set.

Extends ``RuntimeErrorMixin`` and ``Error[MetadataValueType]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata, MetadataValueType


class EntityIdDeletionError(RuntimeErrorMixin, Error[MetadataValueType]):
    """Raised when there is an attempt to delete an entity's identifier."""

    def __init__(self, class_name: str) -> None:
        """Initialise the error with the class name.

        Args:
            class_name: Name of the class whose identifier was targeted for deletion.

        """
        message = ErrorMessage(
            f"Cannot delete 'id' of {class_name} as it defines the entity's identity."
        )
        metadata: ErrorMetadata[MetadataValueType] = ErrorMetadata(
            {
                "class_name": class_name,
                "attribute_name": "id",
            }
        )
        super().__init__(message, metadata)
