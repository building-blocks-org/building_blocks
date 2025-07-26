from pydantic import BaseModel


class AuthenticateUserHttpRequest(BaseModel):
    """
    HTTP request model for user authentication.
    This model is used to validate the incoming request data for user authentication.
    """

    email: str
    password: str
