"""Error raised when an entity ID is None but should not be.

Defines ``EntityIdNoneError``, raised when code attempts to use an identityless
entity in a context that requires a defined identifier.

Extends ``ValueErrorMixin`` and ``Error[MetadataValueType]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata, MetadataValueType


class EntityIdNoneError(ValueErrorMixin, Error[MetadataValueType]):
    """Raised when an entity ID is ``None`` but must be set.

    Entities require an identity for correctness: an entity with
    ``id=None`` cannot participate in equality comparisons, hash-based
    collections, or identity lookups.  This error fires at the point
    where code attempts to use an identityless entity in a context that
    requires a defined identifier.
    Example:
        ```python
        error = EntityIdNoneError("Customer")
        # error.message = "Entity ID have to be defined for 'Customer'."
        ```
    """

    def __init__(self, entity_class_name: str) -> None:
        """Initialise with the class name of the identityless entity.

        Args:
            entity_class_name: The ``__name__`` of the entity class
                whose ``id`` field is ``None``.

        """
        message = ErrorMessage(f"Entity ID have to be defined for '{entity_class_name}'.")
        metadata: ErrorMetadata[MetadataValueType] = ErrorMetadata(
            context={
                "entity_class_name": entity_class_name,
            }
        )
        super().__init__(message=message, metadata=metadata)
