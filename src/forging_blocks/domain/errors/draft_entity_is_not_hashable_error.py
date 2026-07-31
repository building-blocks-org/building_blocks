"""Error raised when a draft entity is used in a context requiring hashability.

Defines ``DraftEntityIsNotHashableError``, raised when a draft entity — one with
``id=None`` that has not yet been assigned an identity — is used in a hashable
context such as a ``set`` or ``dict`` key. Since draft entities lack an identity
by definition, they cannot produce a stable hash value.

Extends ``RuntimeErrorMixin`` and ``Error[MetadataValueType]``.
"""

from typing import Self

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata, MetadataValueType


class DraftEntityIsNotHashableError(RuntimeErrorMixin, Error[MetadataValueType]):
    """Raised because draft entities are not hashable.

    A draft entity has ``id=None`` and therefore cannot produce a
    stable hash. Any operation that requires hashing — membership
    in a ``set``, use as a ``dict`` key, or any hash-based lookup —
    triggers this error. Once the entity receives an identity, hashing
    becomes valid.
    """

    @classmethod
    def from_class_name(cls, class_name: str) -> Self:
        """Create an error from the class name of the draft entity.

        Args:
            class_name: The ``__name__`` of the entity class that was
                used in a hash-requiring context while still a draft.

        Returns:
            A ``DraftEntityIsNotHashableError`` with a descriptive
            message and class-name metadata.

        """
        error_text = f"Unhashable {class_name}: draft entities (id=None) are not hashable"
        error_message = ErrorMessage(error_text)
        metadata: ErrorMetadata[MetadataValueType] = ErrorMetadata({"class_name": class_name})

        return cls(error_message, metadata)
