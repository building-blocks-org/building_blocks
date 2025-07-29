from abc import abstractmethod
from dataclasses import dataclass
from typing import Union

from building_blocks.application.ports.inbound.use_case import AsyncUseCase as UseCase


@dataclass(frozen=True)
class ChangeUserRoleRequest:
    user_id: str
    new_role: str


@dataclass(frozen=True)
class ChangeUserRoleSucceededResponse:
    user_id: str
    previous_role: str
    new_role: str


@dataclass(frozen=True)
class ChangeUserRoleFailedResponse:
    reason: str
    code: str


ChangeUserRoleResponse = Union[
    ChangeUserRoleSucceededResponse, ChangeUserRoleFailedResponse
]


class ChangeUserRoleUseCase(UseCase[ChangeUserRoleRequest, ChangeUserRoleResponse]):
    @abstractmethod
    async def execute(self, request: ChangeUserRoleRequest) -> ChangeUserRoleResponse:
        """
        Execute the use case to change a user's role.
        Args:
            request (ChangeUserRoleRequest): The request containing user ID and new
            role.
        Returns:
            ChangeUserRoleResponse: A Union type response that can either be a
            ChangeUserRoleSucceededResponse or ChangeUserRoleFailedResponse indicating
            success or failure of the operation.
        """
        pass
