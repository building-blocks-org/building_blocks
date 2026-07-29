"""Modules defining validation error classes.

Defines error classes related to validation failures within the system.
"""

from abc import ABC

from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin

from ..core import ErrorMessage, ErrorMetadata
from .error import Error


class ValidationError(ValueErrorMixin, Error[object], ABC):
    """Base class for validation errors — abstract, use ``ValidationFailedError`` to throw."""

    def __init__(
        self, message: ErrorMessage, metadata: ErrorMetadata[object] | None = None
    ) -> None:
        if type(self) is ValidationError:
            raise TypeError("ValidationError is abstract; use ValidationFailedError instead")
        super().__init__(message, metadata)
