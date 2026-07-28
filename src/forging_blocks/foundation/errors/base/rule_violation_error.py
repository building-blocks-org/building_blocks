"""Module defining errors related to rule violations within the system.

Defines error classes for handling rule violation scenarios.
"""

from abc import ABC

from .error import Error


class RuleViolationError(Error[object], ABC):
    """Base class for rule violation errors — abstract, use ``RuleViolated`` to throw."""

    ...
