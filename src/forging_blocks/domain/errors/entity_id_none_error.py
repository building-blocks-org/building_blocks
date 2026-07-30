"""Error raised when an entity ID is None but should not be.

Defines ``EntityIdNoneError``, raised when an entity ID is None but should not be.

Extends ``ValueErrorMixin`` and ``Error[MetadataValueType]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata, MetadataValueType


class EntityIdNoneError(ValueErrorMixin, Error[MetadataValueType]):
    """Raised when an entity ID is None but should not be."""

    def __init__(self, entity_class_name: str) -> None:
        message = ErrorMessage(f"Entity ID have to be defined for '{entity_class_name}'.")
        metadata: ErrorMetadata[MetadataValueType] = ErrorMetadata(
            context={
                "entity_class_name": entity_class_name,
            }
        )
        super().__init__(message=message, metadata=metadata)
