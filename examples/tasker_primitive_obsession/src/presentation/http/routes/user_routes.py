from fastapi import APIRouter, Depends, status

from examples.tasker_primitive_obsession.src.application.ports import (
    AuthenticateUserUseCase,
    ChangeUserRoleUseCase,
    RegisterUserUseCase,
)
from examples.tasker_primitive_obsession.src.presentation.http.dependencies import (
    get_authenticate_user_use_case,
    get_change_user_role_use_case,
    get_register_user_use_case,
)
from examples.tasker_primitive_obsession.src.presentation.http.mappers import (
    AuthenticateUserDtoMapper,
    ChangeUserRoleHttpInput,
    ChangeUserRoleHttpToUseCaseRequestMapper,
    ChangeUserRoleUseCaseToHttpResponseMapper,
    RegisterUserDtoMapper,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    AuthenticateUserHttpRequest,
    ChangeUserRoleHttpRequest,
    RegisterUserHttpRequest,
)
from examples.tasker_primitive_obsession.src.presentation.http.responses import (
    AuthenticateUserHttpResponse,
    ChangeUserRoleHttpResponse,
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


@router.post(
    "/sign_in",
    status_code=status.HTTP_200_OK,
    response_model=AuthenticateUserHttpResponse,
)
async def sign_in_user(
    request: AuthenticateUserHttpRequest,
    use_case: AuthenticateUserUseCase = Depends(get_authenticate_user_use_case),
) -> AuthenticateUserHttpResponse:
    """
    Endpoint to sign in a user.

    Args:
        request (AuthenticateUserHttpRespoonse): The request containing user
        credentials.

    Returns:
        AuthenticateUserHttpResponse: Response containing the access, refresh tokens,
        their expiration times, and token scheme.
    """
    service_request = AuthenticateUserDtoMapper.from_http_request(request)
    service_response = await use_case.execute(service_request)
    response = AuthenticateUserDtoMapper.to_http_response(service_response)

    return response


@router.put(
    "/{user_id}/role",
    status_code=status.HTTP_200_OK,
    response_model=ChangeUserRoleHttpResponse,
)
async def change_user_role(
    request: ChangeUserRoleHttpRequest,
    user_id: str,
    use_case: ChangeUserRoleUseCase = Depends(get_change_user_role_use_case),
) -> ChangeUserRoleHttpResponse:
    """ """
    http_input = ChangeUserRoleHttpInput(
        user_id=user_id,
        request=request,
    )
    service_request = ChangeUserRoleHttpToUseCaseRequestMapper().map(http_input)
    service_response = await use_case.execute(service_request)
    response = ChangeUserRoleUseCaseToHttpResponseMapper().map(service_response)
    return response
