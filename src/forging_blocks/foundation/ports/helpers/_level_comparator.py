"""Compares dependency levels to determine their architectural relation."""

from typing import SupportsIndex, cast

from ._level_relation import LevelRelation


class LevelComparator:
    """Compares dependency levels to determine their architectural relation.

    Responsibilities:
        - Report whether a dependency port sits deeper (``INWARD``),
          shallower (``OUTWARD``), or equal (``SAME``) relative to the
          declaring port's declared level.
        - Report ``UNKNOWN`` when either level is missing or cannot be
          coerced to ``int``, letting callers fall back to legacy rules.

    Non-Responsibilities:
        - Does NOT raise on uncoercible levels — returns ``UNKNOWN``.
        - Does NOT interpret layer vocabulary — only integer ordering.

    Example:
        ```python
        comparator = LevelComparator()

        comparator.compare(0, 2)  # LevelRelation.INWARD
        comparator.compare(2, 0)  # LevelRelation.OUTWARD
        comparator.compare(None, 2)  # LevelRelation.UNKNOWN
        ```
    """

    def compare(self, self_level: object, dep_level: object) -> LevelRelation:
        """Report the relation of dep_level relative to self_level.

        Example:
            ```python
            LevelComparator().compare(Level.OUTERMOST, Level.INNERMOST)
            # LevelRelation.INWARD
            ```
        """
        self_int = self._try_coerce_to_int(self_level)
        dep_int = self._try_coerce_to_int(dep_level)

        if self_int is None or dep_int is None:
            return LevelRelation.UNKNOWN

        return self._determine_relation(dep_int, self_int)

    def _try_coerce_to_int(self, level: object) -> int | None:
        """Attempt to coerce level to int; return None if impossible."""
        if level is None:
            return None
        try:
            return int(cast("SupportsIndex", level))
        except (TypeError, ValueError):
            return None

    def _determine_relation(self, dep_int: int, self_int: int) -> LevelRelation:
        """Determine relation given two validated integers."""
        if dep_int > self_int:
            return LevelRelation.INWARD
        if dep_int < self_int:
            return LevelRelation.OUTWARD
        return LevelRelation.SAME
