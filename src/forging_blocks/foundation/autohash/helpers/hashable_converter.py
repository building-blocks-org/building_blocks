"""Convert arbitrary field values into hashable equivalents.

Ensures that field values such as ``list`` and ``dict`` can
participate in ``__hash__`` computations by converting them to
immutable types.
"""

from collections.abc import Hashable
from typing import cast

from forging_blocks.foundation.errors.non_hashable_value_error import (
    NonHashableValueError,
)


class HashableConverter:
    """Recursively converts non-hashable values to hashable equivalents.

    - ``list`` → ``tuple`` (recursively)
    - ``set`` → ``frozenset``
    - ``dict``  → ``frozenset`` of ``(key, hashable_value)`` pairs (recursively)
    - Already-hashable values (``str``, ``int``, ``None``, ``tuple``,
      ``frozenset``, etc.) are returned unchanged.
    - Everything else raises `NonHashableValueError`.
    """

    @classmethod
    def convert(cls, value: object, field_name: str | None = None) -> Hashable:
        """Convert *value* to a hashable equivalent.

        Uses structural pattern matching for type dispatch, ensuring that
        tuple and frozenset are handled before the generic Hashable arm so
        nested unhashable contents are recursively converted.

        Args:
            value: Any value that may appear as a field on a decorated class.
            field_name: Optional field name where the value was encountered.

        Returns:
            A hashable representation of *value*.

        Raises:
            NonHashableValueError: When *value* cannot be made hashable (e.g. a
                custom non-hashable object).

        """
        match value:
            case tuple():
                converted = (
                    cls.convert(v, field_name=field_name) for v in cast("tuple[object, ...]", value)
                )
                return tuple(converted)
            case frozenset():
                converted = (
                    cls.convert(v, field_name=field_name) for v in cast("frozenset[object]", value)
                )
                return frozenset(converted)
            case _ if isinstance(value, Hashable):
                return value
            case list():
                converted = (
                    cls.convert(v, field_name=field_name) for v in cast("list[object]", value)
                )
                return tuple(converted)
            case dict():
                return frozenset(
                    (k, cls.convert(v, field_name=field_name))
                    for k, v in cast("dict[object, object]", value).items()
                )
            case set():
                converted = (
                    cls.convert(v, field_name=field_name) for v in cast("set[object]", value)
                )
                return frozenset(converted)
            case _:
                raise NonHashableValueError(type(value).__name__, field_name=field_name)
