from dataclasses import asdict
from typing import Any, Dict

from examples.tasker_primitives.src.application.ports import (
    AuthenticateUserRequest,
    AuthenticateUserResponse,
    AuthenticateUserTokenScheme,
    AuthenticateUserUseCase,
    PasswordVerifier,
    TokenGenerator,
    TokenGeneratorPurpose,
    TokenGeneratorRequest,
)
from examples.tasker_primitives.src.domain.ports import UserRepository


class AuthenticateUserService(AuthenticateUserUseCase):
    """
    Service implementation for user authentication.
    This service handles the logic for authenticating a user
    and generating access and refresh tokens.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_verifier: PasswordVerifier,
        access_token_generator: TokenGenerator,
        refresh_token_generator: TokenGenerator,
    ) -> None:
        self._user_repository = user_repository
        self._password_verifier = password_verifier
        self._access_token_generator = access_token_generator
        self._refresh_token_generator = refresh_token_generator

    async def execute(
        self, request: AuthenticateUserRequest
    ) -> AuthenticateUserResponse:
        """
        Execute the use case to authenticate a user.

        Args:
            request (AuthenticateUserUseCase.AuthenticateUserRequest): The request
            containing user credentials.

        Returns:
            AuthenticateUserResponse: The response containing access and refresh tokens.
        """
        user = await self._user_repository.find_by_email(request.email)

        if not user:
            raise ValueError("User not found")

        if not self._password_verifier.verify(request.password, user.password):
            raise ValueError("Invalid password")

        stringed_user_id = str(user.id)
        access_token = self._generate_access_token(stringed_user_id)
        refresh_token = self._generate_refresh_token(stringed_user_id)

        return AuthenticateUserResponse(
            access_token=access_token["token"],
            access_token_expires_in=access_token["expires_in"],
            refresh_token=refresh_token["token"],
            refresh_token_expires_in=refresh_token["expires_in"],
            token_scheme=AuthenticateUserTokenScheme.BEARER,
        )

    def _generate_access_token(self, user_id: str) -> Dict[str, Any]:
        """
        Generate an access token for the authenticated user.

        Args:
            user_id (str): The ID of the authenticated user.
        Returns:
            Dict[str, Any]: A dictionary containing the access token and its expiration
            time.
            The keys are `token`(string) and `expires_in`(int).
        """
        request = TokenGeneratorRequest(user_id, TokenGeneratorPurpose.ACCESS)

        return asdict(self._access_token_generator.generate(request))

    def _generate_refresh_token(self, user_id: str) -> Dict[str, Any]:
        """
        Generate a refresh token for the authenticated user.

        Args:
            user_id (str): The ID of the authenticated user.
        Returns:
            Dict[str, Any]: A dictionary containing the refresh token and its expiration
            time.
            The keys are `token`(string) and `expires_in`(int).
        """
        request = TokenGeneratorRequest(user_id, TokenGeneratorPurpose.REFRESH)

        return asdict(self._access_token_generator.generate(request))
