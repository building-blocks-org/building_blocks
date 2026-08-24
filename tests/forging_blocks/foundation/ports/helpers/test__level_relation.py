"""Tests for the LevelRelation enum."""

import pytest

from forging_blocks.foundation.ports.helpers._level_relation import LevelRelation


@pytest.mark.unit
class TestLevelRelation:
    def test_has_exactly_the_four_directional_members(self) -> None:
        assert [member.name for member in LevelRelation] == [
            "INWARD",
            "OUTWARD",
            "SAME",
            "UNKNOWN",
        ]

    def test_members_are_distinct(self) -> None:
        assert len(set(LevelRelation)) == 4
