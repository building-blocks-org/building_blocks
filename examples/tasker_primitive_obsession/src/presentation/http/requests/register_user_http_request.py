from pydantic import BaseModel


class RegisterUserHttpRequest(BaseModel):
    """
    Request model for registering a new user.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password for the user account.
        role (str): The role of the user, default is "engineer".
    """

    name: str
    email: str
    password: str
    role: str = "engineer"
