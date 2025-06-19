from abc import ABC, abstractmethod
from dataclasses import dataclass

from building_blocks.application.ports.inbound.use_case import AsyncUseCase


@dataclass(frozen=True)
class CreateTaskRequest:
    title: str
    description: str
    due_date: str
    priority: int


@dataclass(frozen=True)
class CreateTaskResponse:
    task_id: str


class CreateTaskUseCase(AsyncUseCase[CreateTaskRequest, CreateTaskResponse], ABC):
    """
    Use case for creating a new task.

    This use case handles the creation of a new task based on the provided request data.
    It returns a response containing the ID of the newly created task.
    """

    @abstractmethod
    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Execute the use case to create a new task.

        :param request: The request data containing task details.
        :return: A response containing the ID of the created task.
        """
        raise NotImplementedError("Method not implemented")
