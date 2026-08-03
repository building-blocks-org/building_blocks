from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorMessage:
    """Represents an immutable error message component.

    Example:
        ```python
        msg = ErrorMessage("Something went wrong")
        assert msg.value == "Something went wrong"
        ```
    """

    value: str
