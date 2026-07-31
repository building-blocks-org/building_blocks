"""Error raised when a specification predicate is not a callable object.

Defines ``NotCallablePredicateError``, raised when an object provided
as a specification predicate is not callable.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, MetadataValueType


class NotCallablePredicateError(ValueErrorMixin, Error[MetadataValueType]):
    """Exception raised when a specification predicate is not callable.

    The error message includes the actual type of the predicate that was
    provided, helping developers identify and fix the issue.

    Attributes:
        message: Structured error message containing the type name of the invalid predicate.
        metadata: Optional metadata providing additional context about the error.
        context: Shortcut access to the metadata context dictionary.
    """

    def __init__(
        self,
        predicate: object,
    ) -> None:
        """Initialize the NotCallablePredicateError with the invalid predicate.

        Args:
            predicate: The object that was provided as a predicate but is not callable.
                The type name of this object will be included in the error message.

        """
        message = ErrorMessage(f"predicate must be Callable and not {type(predicate).__name__}")
        super().__init__(message)
