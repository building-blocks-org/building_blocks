"""Direction of a declared dependency relative to the declaring port."""

from enum import Enum


class LevelRelation(Enum):
    """Direction of a declared dependency relative to the declaring port."""

    INWARD = 0
    OUTWARD = 1
    SAME = 2
    UNKNOWN = 3
