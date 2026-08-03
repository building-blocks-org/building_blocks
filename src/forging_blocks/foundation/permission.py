"""Granular permission identifiers for authorization checks."""

from enum import StrEnum


class Permission(StrEnum):
    """Granular permission identifiers for authorization checks.

    Example:
        ```python
        from forging_blocks.foundation.permission import Permission

        perm = Permission.READ
        assert perm == "read"
        assert isinstance(perm, str)
        ```
    """

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
