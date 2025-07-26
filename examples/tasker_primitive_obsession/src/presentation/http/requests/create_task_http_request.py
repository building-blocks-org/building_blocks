import datetime
from typing import List, Optional

from pydantic import BaseModel


class CreateTaskHttpRequest(BaseModel):
    """
    Request model for creating a new task.

    Attributes:
        title (str): The title of the task.
        description (str): A brief description of the task.
        due_date (str): The due date for the task in ISO format (YYYY-MM-DD).
    """

    title: str
    description: str
    due_date: datetime.date  # ISO format date string
    priority: str
    tags: Optional[List[str]] = None
    progresss: int = 0
    assignee_email: Optional[str] = None
