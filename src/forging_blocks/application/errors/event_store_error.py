"""Event store error type for application-level operations."""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.core import ErrorMessage


class EventStoreError[MetadataValueType = object](Error[MetadataValueType]):
    """Base error for event store operations."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
