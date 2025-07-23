from abc import abstractmethod
from dataclasses import dataclass

from building_blocks.application.ports.inbound.use_case import AsyncUseCase as UseCase


@dataclass(frozen=True)
class AuthenticateUserRequest:
    email: str
    password: str


@dataclass(frozen=True)
class AuthenticateUserResponse:
    access_token: str
    access_token_expires_in: int
    refresh_token: str
    refresh_token_expires_in: int
    token_scheme: str = "Bearer"


class AuthenticateUserUseCase(
    UseCase[AuthenticateUserRequest, AuthenticateUserResponse]
):
    @abstractmethod
    async def execute(
        self, request: AuthenticateUserRequest
    ) -> AuthenticateUserResponse:
        """
        Execute the use case to authenticate a user.

        Args:
            request (AuthenticateUserRequest): The request containing user credentials.

        Returns:
            AuthenticateUserResponse: The response containing access and refresh tokens.
        """
        pass
