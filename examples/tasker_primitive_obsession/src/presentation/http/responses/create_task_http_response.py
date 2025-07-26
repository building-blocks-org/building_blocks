from pydantic import BaseModel


class CreateTaskHttpResponse(BaseModel):
    """
    Response model for creating a new task.

    Attributes:
        task_id (str): The unique identifier of the created task.
    """

    task_id: str
