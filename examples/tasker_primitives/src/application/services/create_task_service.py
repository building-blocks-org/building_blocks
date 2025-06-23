import uuid

from examples.tasker_primitives.src.application.ports import (
    CreateTaskRequest,
    CreateTaskResponse,
    CreateTaskUseCase,
)
from examples.tasker_primitives.src.domain.entities.task import Task
from examples.tasker_primitives.src.domain.ports.outbound.task_repository import (
    TaskRepository,
)


class CreateTaskService(CreateTaskUseCase):
    """
    Service implementation for creating tasks.

    This service handles the creation of tasks by interacting with the
    TaskRepository to persist the task data.
    """

    def __init__(self, task_repository: TaskRepository) -> None:
        """
        Initialize the service with a task repository.

        Args:
            task_repository: The repository to handle task persistence.
        """
        self._task_repository = task_repository

    async def execute(self, request: CreateTaskRequest) -> CreateTaskResponse:
        """
        Execute the use case to create a new task.

        Args:
            request (CreateTaskRequest): The request containing task details.

        Returns:
            CreateTaskResponse: The response containing the created task ID.
        """
        task_id = uuid.uuid4()
        task = Task(
            task_id=task_id,
            title=request.title,
            description=request.description,
            due_date=request.due_date,
        )
        await self._task_repository.save(task)

        return CreateTaskResponse(task_id=str(task.id))
