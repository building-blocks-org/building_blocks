"""Modules defining validation error classes.

Defines error classes related to validation failures within the system.
"""

from abc import ABC

from .error import Error


class ValidationError(Error[object], ABC):
    """Base class for validation errors — abstract, use ``ValidationFailed`` to throw."""
