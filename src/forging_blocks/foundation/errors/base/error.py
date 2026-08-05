"""Fundamental error class for the Building Blocks framework.

Defines the base Error type that all structured errors inherit from.
"""

from typing import Self

from forging_blocks.foundation.debuggable import Debuggable

from ..core import ErrorMessage, ErrorMetadata


class Error[MetadataValueType](Exception, Debuggable):
    """Base class for all structured errors that can be raised like standard Exceptions.

    Example:
        ```python
        msg = ErrorMessage("Not found")
        meta = ErrorMetadata[str](context={"id": "42"})
        error = Error[str](msg, meta)
        print(error.message.value)  # "Not found"
        print(error.context)  # {"id": "42"}
        raise error  # subclass of Exception
        ```
    """

    def __init__(
        self, message: ErrorMessage, metadata: ErrorMetadata[MetadataValueType] | None = None
    ) -> None:
        """Initialise the error with a structured message and optional metadata.

        Args:
            message: The structured error message describing what went wrong.
            metadata: Optional structured metadata with additional diagnostic
                context. Defaults to an empty `ErrorMetadata` when
                not provided.

        """
        super().__init__(message.value)
        self._message = message
        self._metadata = metadata or ErrorMetadata[MetadataValueType]()

    @classmethod
    def from_string(
        cls,
        text: str,
        metadata: ErrorMetadata[MetadataValueType] | None = None,
    ) -> Self:
        """Create an error from a plain message string.

        Convenience factory that wraps ``text`` in an ``ErrorMessage``
        and passes it to the constructor. All ``Error`` subclasses
        inherit this method so callers can raise errors without
        manually constructing ``ErrorMessage`` instances.

        Args:
            text: The raw error message text.
            metadata: Optional structured metadata with diagnostic context.

        Returns:
            A new error instance.

        Example:
            ```python
            class PaymentError(Error[str]):
                pass


            error = PaymentError.from_string("Insufficient funds")
            raise error
            ```

        """
        return cls(ErrorMessage(text), metadata)

    def __str__(self) -> str:
        context_str = f" | Context: {self._metadata.context}" if self._metadata.context else ""
        return f"{self.__class__.__name__}: {self._message.value}{context_str}"

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} message={self._message.value!r} "
            f"context={self._metadata.context!r}>"
        )

    @property
    def message(self) -> ErrorMessage:
        """Structured error message."""
        return self._message

    @property
    def metadata(self) -> ErrorMetadata[MetadataValueType]:
        """Structured metadata with additional context."""
        return self._metadata

    @property
    def context(self) -> dict[str, MetadataValueType]:
        """Shortcut for accessing the metadata context."""
        return self._metadata.context

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string for debugging."""
        return (
            f"{self.__class__.__name__}(\n"
            f"  message={repr(self._message)},\n"
            f"  metadata={repr(self._metadata)}\n"
            ")"
        )
