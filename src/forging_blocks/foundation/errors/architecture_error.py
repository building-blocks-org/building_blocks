"""Architecture error for dependency direction violations.

Defines ``ArchitectureError``, raised at class-definition time when a subclass
violates Clean Architecture dependency rules.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, MetadataValueType


class ArchitectureError(RuntimeErrorMixin, Error[MetadataValueType]):
    """Raised when a subclass violates dependency direction rules.

    Clean Architecture requires that dependencies flow inward: outer
    layers may depend on inner layers, but never the reverse. This error
    fires at class creation time via ``__init_subclass__`` whenever a
    subclass declares a dependency that points in the wrong direction.
    """

    def __init__(self, message: str) -> None:
        """Initialise with a descriptive violation message.

        Args:
            message: Human-readable description of the violation,
                including the class name, the offending parameter,
                and the applicable rule.

        """
        super().__init__(ErrorMessage(message))
