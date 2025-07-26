from examples.tasker_primitive_obsession.src.application.ports import (
    RegisterUserRequest,
    RegisterUserResponse,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    RegisterUserHttpRequest,
)
from examples.tasker_primitive_obsession.src.presentation.http.responses import (
    RegisterUserHttpResponse,
)


class RegisterUserDtoMapper:
    @staticmethod
    def from_http_request(request: RegisterUserHttpRequest) -> RegisterUserRequest:
        return RegisterUserRequest(
            name=request.name,
            email=request.email,
            password=request.password,
            role=request.role,
        )

    @staticmethod
    def to_http_response(response: RegisterUserResponse) -> RegisterUserHttpResponse:
        return RegisterUserHttpResponse(user_id=response.user_id)
