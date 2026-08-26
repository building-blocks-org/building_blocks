"""Tests for the PortLevel base ordering."""

import pytest

from forging_blocks.foundation.ports import PortLevel


class Level(PortLevel):
    OUTERMOST = 0
    MIDDLE = 1
    INNERMOST = 2


@pytest.mark.unit
class TestPortLevel:
    def test_ordering_by_int(self) -> None:
        """Members order by their integer depth, and raw ints interoperate."""

        assert int(Level.MIDDLE) == 1
        assert Level.MIDDLE < Level.INNERMOST
        assert int(3) > int(Level.INNERMOST)

    def test_no_preset_members(self) -> None:
        """The library ships no preset layer vocabulary."""

        assert not hasattr(PortLevel, "APPLICATION")
