"""Base error for event persistence operations.

Defines ``EventStoreError``, raised when append, read, or snapshot
operations on the event store fail. Extends ``RuntimeErrorMixin``,
making it catchable as ``RuntimeError``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage


class EventStoreError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Base error for event store operations."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
