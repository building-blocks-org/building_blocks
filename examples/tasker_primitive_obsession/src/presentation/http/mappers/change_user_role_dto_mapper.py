from dataclasses import dataclass

from building_blocks.abstractions.mapper import Mapper
from examples.tasker_primitive_obsession.src.application.ports import (
    ChangeUserRoleFailedResponse,
    ChangeUserRoleRequest,
    ChangeUserRoleResponse,
    ChangeUserRoleSucceededResponse,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    ChangeUserRoleHttpRequest,
)
from examples.tasker_primitive_obsession.src.presentation.http.responses import (
    ChangeUserRoleFailedHttpResponse,
    ChangeUserRoleHttpResponse,
    ChangeUserRoleSucceededHttpResponse,
)


@dataclass(frozen=True)
class ChangeUserRoleHttpInput:
    user_id: str
    request: ChangeUserRoleHttpRequest


class ChangeUserRoleHttpToUseCaseRequestMapper(
    Mapper[ChangeUserRoleHttpInput, ChangeUserRoleRequest]
):
    def map(self, source: ChangeUserRoleHttpInput) -> ChangeUserRoleRequest:
        return ChangeUserRoleRequest(
            user_id=source.user_id, new_role=source.request.new_role
        )


class ChangeUserRoleUseCaseToHttpResponseMapper(
    Mapper[ChangeUserRoleResponse, ChangeUserRoleHttpResponse]
):
    def map(self, response: ChangeUserRoleResponse) -> ChangeUserRoleHttpResponse:
        if isinstance(response, ChangeUserRoleSucceededResponse):
            return ChangeUserRoleSucceededHttpResponse(
                user_id=response.user_id,
                previous_role=response.previous_role,
                new_role=response.new_role,
            )
        elif isinstance(response, ChangeUserRoleFailedResponse):
            return ChangeUserRoleFailedHttpResponse(
                reason=response.reason, code=response.code
            )
        else:
            raise ValueError("Unexpected response type from ChangeUserRoleUseCase")
