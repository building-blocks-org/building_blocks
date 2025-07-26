from pydantic import BaseModel


class RegisterUserHttpResponse(BaseModel):
    """
    Response model for registering a new user.

    Attributes:
        user_id (str): The unique identifier of the registered user.
    """

    user_id: str
