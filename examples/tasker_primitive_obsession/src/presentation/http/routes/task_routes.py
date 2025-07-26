from fastapi import APIRouter, Depends, status

from examples.tasker_primitive_obsession.src.application.ports import (
    CreateTaskUseCase,
)
from examples.tasker_primitive_obsession.src.presentation.http.dependencies import (
    get_create_task_use_case,
)
from examples.tasker_primitive_obsession.src.presentation.http.mappers import (
    CreateTaskDtoMapper,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    CreateTaskHttpRequest,
)
from examples.tasker_primitive_obsession.src.presentation.http.responses import (
    CreateTaskHttpResponse,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "", status_code=status.HTTP_201_CREATED, response_model=CreateTaskHttpResponse
)
async def create_task(
    request: CreateTaskHttpRequest,
    use_case: CreateTaskUseCase = Depends(get_create_task_use_case),
) -> CreateTaskHttpResponse:
    service_request = CreateTaskDtoMapper.from_http_request(request)
    service_response = await use_case.execute(service_request)
    response = CreateTaskDtoMapper.to_http_response(service_response)

    return response
