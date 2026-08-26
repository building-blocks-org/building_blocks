"""Tests for the LevelComparator helper."""

import pytest

from forging_blocks.foundation.ports import PortLevel
from forging_blocks.foundation.ports.helpers._level_comparator import (
    LevelComparator,
)
from forging_blocks.foundation.ports.helpers._level_relation import LevelRelation


class Level(PortLevel):
    OUTERMOST = 0
    MIDDLE = 1
    INNERMOST = 2


@pytest.mark.unit
class TestLevelComparator:
    def test_returns_inward_when_dependency_is_deeper(self) -> None:
        relation = LevelComparator().compare(Level.OUTERMOST, Level.INNERMOST)

        assert relation is LevelRelation.INWARD

    def test_returns_outward_when_dependency_is_shallower(self) -> None:
        relation = LevelComparator().compare(Level.INNERMOST, Level.OUTERMOST)

        assert relation is LevelRelation.OUTWARD

    def test_returns_same_when_levels_are_equal(self) -> None:
        relation = LevelComparator().compare(Level.MIDDLE, Level.MIDDLE)

        assert relation is LevelRelation.SAME

    def test_interoperates_with_raw_ints(self) -> None:
        comparator = LevelComparator()

        assert comparator.compare(0, 2) is LevelRelation.INWARD
        assert comparator.compare(2, 0) is LevelRelation.OUTWARD
        assert comparator.compare(1, 1) is LevelRelation.SAME

    def test_returns_unknown_when_self_level_is_missing(self) -> None:
        relation = LevelComparator().compare(None, Level.INNERMOST)

        assert relation is LevelRelation.UNKNOWN

    def test_returns_unknown_when_dependency_level_is_missing(self) -> None:
        relation = LevelComparator().compare(Level.OUTERMOST, None)

        assert relation is LevelRelation.UNKNOWN

    def test_returns_unknown_when_level_is_uncoercible(self) -> None:
        relation = LevelComparator().compare(Level.OUTERMOST, object())

        assert relation is LevelRelation.UNKNOWN
