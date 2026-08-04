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
        class User:
            def __init__(self, roles: set[Permission]) -> None:
                self.roles = roles


        class ReadChecker(PermissionChecker[User]):
            async def check(self, context: User, permission: Permission) -> bool:
                return permission == Permission.READ


        class WriteChecker(PermissionChecker[User]):
            async def check(self, context: User, permission: Permission) -> bool:
                return permission == Permission.WRITE


        composite = CompositePermissionChecker([ReadChecker(), WriteChecker()])
        user = User(roles={Permission.READ})
        granted = await composite.check(user, Permission.READ)
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
