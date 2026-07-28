"""Module defining errors related to rule violations within the system.

Defines error classes for handling rule violation scenarios.
"""

from abc import ABC

from ..core import ErrorMessage, ErrorMetadata
from .error import Error


class RuleViolationError(Error[object], ABC):
    """Base class for rule violation errors — abstract, use ``RuleViolatedError`` to throw."""

    def __init__(
        self, message: ErrorMessage, metadata: ErrorMetadata[object] | None = None
    ) -> None:
        if type(self) is RuleViolationError:
            raise TypeError("RuleViolationError is abstract; use RuleViolatedError instead")
        super().__init__(message, metadata)
