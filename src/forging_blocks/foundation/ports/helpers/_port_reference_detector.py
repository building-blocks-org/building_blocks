"""Detect port type references in type annotations.

Recursively unwraps generic aliases, union types, and nested
parameterised generics to determine whether any component references
a specific port type.
"""

from types import UnionType
from typing import get_args, get_origin


class PortReferenceDetector:
    """Detects whether a type annotation references a specific port type.

    Example:
        ```python
        class MyBase: ...


        class MySubclass(MyBase): ...


        detector = PortReferenceDetector(target_port=MyBase)
        detector.detects_in(MySubclass)  # True (MyBase in MRO)
        detector.detects_in(str)  # False
        ```
    """

    def __init__(self, target_port: type) -> None:
        self._target_port = target_port

    def detects_in(self, parameter_type: object) -> bool:
        """Return ``True`` when *parameter_type* references the target port."""
        return bool(self.referenced_ports(parameter_type))

    def referenced_ports(self, parameter_type: object) -> set[type]:
        """Return every port class in *parameter_type* (target or subclass)."""
        found: set[type] = set()
        self._collect(parameter_type, found)
        return found

    def _collect(self, parameter_type: object, found: set[type]) -> None:
        if isinstance(parameter_type, UnionType):
            for argument in get_args(parameter_type):
                self._collect(argument, found)
            return
        if isinstance(parameter_type, type) and self._target_port in parameter_type.__mro__:
            found.add(parameter_type)
            return
        origin = get_origin(parameter_type)
        if origin is not None and origin is not parameter_type:
            for argument in get_args(parameter_type):
                self._collect(argument, found)
