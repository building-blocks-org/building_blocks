from dataclasses import dataclass


@dataclass(frozen=True)
class ErrorMessage:
    """Represents an immutable error message component."""

    value: str
