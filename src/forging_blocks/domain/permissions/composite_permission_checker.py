"""Composite permission checker with OR logic."""

from __future__ import annotations

from forging_blocks.domain.permissions.permission_checker import PermissionChecker
from forging_blocks.foundation.permission import Permission


class CompositePermissionChecker[PermissionCheckContext](PermissionChecker[PermissionCheckContext]):
    """Combines multiple `PermissionChecker` instances with OR logic.

    Type Args:
        PermissionCheckContext: The application-defined context for permission checks.

    Example:
        ```python
        from forging_blocks.domain.permissions.composite_permission_checker import (
            CompositePermissionChecker,
        )
        from forging_blocks.domain.permissions.permission_checker import PermissionChecker
        from forging_blocks.foundation.permission import Permission


        class ReadChecker(PermissionChecker[object]):
            async def check(self, context: object, permission: Permission) -> bool:
                return permission == Permission.READ


        class WriteChecker(PermissionChecker[object]):
            async def check(self, context: object, permission: Permission) -> bool:
                return permission == Permission.WRITE


        composite = CompositePermissionChecker([ReadChecker(), WriteChecker()])
        granted = await composite.check(None, Permission.READ)
        ```
    """

    __match_args__ = ("_checkers",)

    def __init__(self, checkers: list[PermissionChecker[PermissionCheckContext]]) -> None:
        self._checkers = checkers

    async def check(self, context: PermissionCheckContext, permission: Permission) -> bool:
        for checker in self._checkers:
            if await checker.check(context, permission):
                return True
        return False
