"""Error raised when an optimistic concurrency check detects a version conflict.

Indicates that an expected version does not match the current stored version
for an aggregate, meaning another writer committed a change between the
read and write phases of an operation.
"""

from uuid import UUID

from forging_blocks.application.errors.event_store_error import EventStoreError


class ConcurrencyError[MetadataValueType = object](EventStoreError[MetadataValueType]):
    """Raised when an optimistic concurrency check fails.

    Captures the conflicting aggregate identity and the expected
    versus actual version numbers so callers can decide whether to
    retry, reconcile, or fail the operation.

    Attributes:
        aggregate_id: The aggregate that experienced the conflict.
        expected_version: The version the caller expected.
        actual_version: The version currently stored.


    Example:
        ```python
        error = ConcurrencyError(
            aggregate_id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
            expected_version=1,
            actual_version=2,
        )
        raise error
        ```
    """

    def __init__(self, aggregate_id: UUID, expected_version: int, actual_version: int) -> None:
        """Initialise with the conflicting aggregate and version details.

        Args:
            aggregate_id: The identifier of the aggregate with the conflict.
            expected_version: The version number the caller expected to find.
            actual_version: The version number actually stored.

        """
        self.aggregate_id = aggregate_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"Concurrency conflict for aggregate {aggregate_id}: "
            f"expected version {expected_version}, actual {actual_version}"
        )
