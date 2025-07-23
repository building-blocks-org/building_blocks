from fastapi import APIRouter, Depends, status

from examples.tasker_primitives.src.application.ports import RegisterUserUseCase
from examples.tasker_primitives.src.presentation.http.dependencies import (
    get_register_user_use_case,
)
from examples.tasker_primitives.src.presentation.http.mappers import (
    RegisterUserDtoMapper,
)
from examples.tasker_primitives.src.presentation.http.requests import (
    RegisterUserHttpRequest,
)
from examples.tasker_primitives.src.presentation.http.responses import (
    RegisterUserHttpResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterUserHttpResponse,
)
async def register_user(
    request: RegisterUserHttpRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
) -> RegisterUserHttpResponse:
    """
    Endpoint to register a new user.

    Args:
        request (RegisterUserHttpRespoonse): The request containing user details.

    Returns:
        RegisterUserHttpRespoonse: The response containing the registered user ID.
    """
    service_request = RegisterUserDtoMapper.from_http_request(request)
    service_response = await use_case.execute(service_request)
    response = RegisterUserDtoMapper.to_http_response(service_response)

    return response
