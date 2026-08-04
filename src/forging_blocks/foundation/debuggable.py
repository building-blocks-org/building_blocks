"""Module defining a protocol for debuggable objects."""

from typing import Protocol


class Debuggable(Protocol):
    """Protocol for objects that can provide detailed debug string representations.

    Example:
        ```python
        class Invoice(Debuggable):
            def __init__(self, number: str, total: int) -> None:
                self.number = number
                self.total = total

            def as_debug_string(self) -> str:
                return f"Invoice({self.number}, total={self.total})"


        inv = Invoice("INV-001", 4200)
        print(inv.as_debug_string())
        ```
    """

    def as_debug_string(self) -> str:
        """Return a detailed, multi-line string describing this object for debugging."""
        ...
