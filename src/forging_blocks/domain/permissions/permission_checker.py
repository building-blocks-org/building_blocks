"""Protocol for permission-checking implementations."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from forging_blocks.foundation.permission import Permission


@runtime_checkable
class PermissionChecker[PermissionCheckContext](Protocol):
    """Protocol for any callable that decides whether a permission is granted.

    Type Args:
        PermissionCheckContext: The application-defined context for permission checks.

    Example:
        ```python
        from forging_blocks.domain.permissions.permission_checker import PermissionChecker
        from forging_blocks.foundation.permission import Permission


        class MyChecker(PermissionChecker[dict]):
            async def check(self, context: dict, permission: Permission) -> bool:
                return permission in context.get("grants", set())


        checker = MyChecker()
        result = await checker.check({"grants": {Permission.READ}}, Permission.READ)
        ```
    """

    async def check(self, context: PermissionCheckContext, permission: Permission) -> bool:
        """Return ``True`` if *permission* is granted in *context*."""
        ...
