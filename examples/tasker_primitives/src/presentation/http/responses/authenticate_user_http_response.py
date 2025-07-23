from pydantic import BaseModel


class AuthenticateUserHttpResponse(BaseModel):
    """
    HTTP response model for user authentication.
    """

    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    token_scheme: str
