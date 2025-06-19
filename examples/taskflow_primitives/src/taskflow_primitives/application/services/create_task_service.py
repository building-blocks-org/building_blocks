from taskflow_primitives.application.ports.inbound.create_task_use_case import (
    CreateTaskRequest,
    CreateTaskResponse,
    CreateTaskUseCase,
)
from taskflow_primitives.domain.entities.task import Task
from taskflow_primitives.domain.ports.outbound.task_repository import TaskRepository


class CreateTaskService(CreateTaskUseCase):
    def __init__(self, task_repository: TaskRepository) -> None:
        """
        Initialize the CreateTaskService with a TaskRepository.

        :param task_repository: The repository to interact with Task entities.
        """
        self._task_repository = task_repository

    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Execute the use case to create a new task.

        :param request: The request data containing task details.
        :return: A response containing the ID of the created task.
        """
        task = Task.create_pending(
            title=request.title,
            description=request.description,
            due_date=request.due_date,
            priority=request.priority,
        )
        await self._task_repository.save(task)

        return CreateTaskResponse(task_id=task.id_)
