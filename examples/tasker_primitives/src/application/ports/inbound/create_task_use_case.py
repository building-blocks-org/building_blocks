import datetime
from abc import abstractmethod
from dataclasses import dataclass

from building_blocks.application.ports.inbound.use_case import AsyncUseCase as UseCase


@dataclass(frozen=True)
class CreateTaskRequest:
    title: str
    description: str
    due_date: datetime.date


@dataclass(frozen=True)
class CreateTaskResponse:
    task_id: str


class CreateTaskUseCase(UseCase[CreateTaskRequest, CreateTaskResponse]):
    @abstractmethod
    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Execute the use case to create a new task.

        Args:
            request (CreateTaskRequest): The request containing task details.

        Returns:
            CreateTaskResponse: The response containing the created task ID.
        """
        pass
