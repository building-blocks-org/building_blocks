"""Base error for event bus publishing and dispatch failures.

Defines ``EventBusError``, raised when event handlers fail or the message bus
cannot deliver an event. Extends ``RuntimeErrorMixin``, making it catchable as
``RuntimeError``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage


class EventBusError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Base error for event bus operations."""

    def __init__(self, message: str) -> None:
        super().__init__(ErrorMessage(message))
