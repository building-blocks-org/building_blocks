from dataclasses import dataclass


@dataclass(frozen=True)
class FieldReference:
    """Represents a reference to a field in the error message."""

    value: str
