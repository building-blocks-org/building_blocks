from dataclasses import dataclass


@dataclass(frozen=True)
class FieldReference:
    """Represents a reference to a field in the error message.

    Example:
        ```python
        ref = FieldReference("email")
        assert ref.value == "email"
        ```
    """

    value: str
