from examples.tasker_primitives.src.application.ports import (
    CreateTaskRequest,
    CreateTaskResponse,
)
from examples.tasker_primitives.src.presentation.http.requests import (
    CreateTaskHttpRequest,
)
from examples.tasker_primitives.src.presentation.http.responses import (
    CreateTaskHttpResponse,
)


class CreateTaskDtoMapper:
    """
    Mapper class to convert a request object into a task creation dictionary.
    """

    @staticmethod
    def from_http_request(request: CreateTaskHttpRequest) -> CreateTaskRequest:
        """
        Maps the request object to a task creation dictionary.

        :param request: The request object containing task details.
        :return: A dictionary with task creation parameters.
        """

        print(f"Mapping HTTP request to service request: {request}")
        print(f"Request due_date: {request.due_date}")

        return CreateTaskRequest(
            title=request.title,
            description=request.description,
            due_date=request.due_date,
        )

    @staticmethod
    def to_http_response(response: CreateTaskResponse) -> CreateTaskHttpResponse:
        """
        Maps the response object to a HTTP request object.

        :param response: The response object containing task details.
        :return: A HTTP request object with task creation parameters.
        """

        return CreateTaskHttpResponse(
            task_id=response.task_id,
        )
