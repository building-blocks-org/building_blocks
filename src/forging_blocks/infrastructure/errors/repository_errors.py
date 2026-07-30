"""Error classes for repository-level storage operations.

Provides structured error types for save failures, deletion of
non-existent aggregates, and retrieval errors.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage


class RepositoryError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Generic error raised when a repository operation fails.

    This is the base error for all repository-level failures. Concrete
    implementations may raise this or more specific subclasses.
    """


class RepositoryNotFoundError[MetadataValueType = object](RepositoryError[MetadataValueType]):
    """Error raised when attempting to delete or retrieve an aggregate that does not exist."""

    @classmethod
    def for_id(cls, entity_id: object) -> "RepositoryNotFoundError[MetadataValueType]":
        """Create an error for a specific missing aggregate ID.

        Args:
            entity_id: The identifier that was not found.

        Returns:
            A RepositoryNotFoundError with a descriptive message.

        """
        return cls(ErrorMessage(f"Aggregate with id '{entity_id}' not found."))
