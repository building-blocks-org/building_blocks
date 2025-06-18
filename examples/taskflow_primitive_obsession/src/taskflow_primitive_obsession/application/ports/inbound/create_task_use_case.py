from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from building_blocks.application.ports.inbound.use_case import AsyncUseCase


@dataclass(frozen=True)
class CreateTaskRequest:
    """
    Request object for creating a new task.

    Attributes:
        name (str): Name of the task.
        description (str): Description of the task.
        priority (str): Priority level of the task.
        due_date (datetime): Due date for the task.
        assigned_to_email (Optional[str]): Email of the user assigned to the task.
    """

    name: str
    description: str
    priority: str
    due_date: datetime
    assigned_to_email: Optional[str] = None


@dataclass(frozen=True)
class CreateTaskResponse:
    """
    Response object for the CreateTask use case.

    Attributes:
        task_id (str): The ID of the created task.
    """

    task_id: str


class CreateTaskUseCase(AsyncUseCase[CreateTaskRequest, CreateTaskResponse], ABC):
    """
    Use case for creating a new task.

    This use case handles the creation of a new task with the provided details.

    Attributes:
        request (CreateTaskRequest): The request object containing task details.

    Methods:
        execute(request: CreateTaskRequest) -> str: Executes the use case and returns
        the ID of the created task.
    """

    @abstractmethod
    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        pass
