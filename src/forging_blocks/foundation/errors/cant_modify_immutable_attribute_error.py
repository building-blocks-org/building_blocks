"""Module for CantModifyImmutableAttributeError exception."""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.core import ErrorMessage, ErrorMetadata


class CantModifyImmutableAttributeError(Error[str]):
    """Raised when there is an attempt to modify an immutable attribute of an object."""

    def __init__(self, class_name: str, attribute_name: str):
        """Initialise the error with the class and attribute that triggered the violation.

        Args:
            class_name: Name of the class whose immutable attribute was targeted.
            attribute_name: Name of the attribute that was being modified.

        """
        message = ErrorMessage(
            f"Cannot modify immutable attribute '{attribute_name}' of class '{class_name}'."
        )
        super().__init__(
            message,
            ErrorMetadata({"class_name": class_name, "attribute_name": attribute_name}),
        )
