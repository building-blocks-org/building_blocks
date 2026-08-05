"""Abstract base class for business rule violation errors.

Defines ``RuleViolationError``, an abstract base for errors raised when
business rules or invariants are violated. It extends ``RuntimeErrorMixin``
(making it catchable as ``RuntimeError``) and ``Error[object]`` for
mixed-context metadata.

Cannot be instantiated directly — use the concrete ``RuleViolatedError``
to raise rule violation errors.
"""

from abc import ABC

from ..builtin.runtime_error_mixin import RuntimeErrorMixin
from ..core import ErrorMessage, ErrorMetadata
from .error import Error


class RuleViolationError(RuntimeErrorMixin, Error[object], ABC):
    """Base class for rule violation errors — abstract, use ``RuleViolatedError`` to throw.

    Example:
        ```python
        class RuleViolated(RuleViolationError[object]):
            pass


        error = RuleViolated.from_string("Insufficient funds")
        ```

    """

    def __init__(
        self, message: ErrorMessage, metadata: ErrorMetadata[object] | None = None
    ) -> None:
        if type(self) is RuleViolationError:
            raise TypeError("RuleViolationError is abstract; use RuleViolatedError instead")
        super().__init__(message, metadata)
