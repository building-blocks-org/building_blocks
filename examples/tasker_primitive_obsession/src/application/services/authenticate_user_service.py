import logging

from examples.tasker_primitive_obsession.src.application.ports import (
    AuthenticateUserRequest,
    AuthenticateUserResponse,
    AuthenticateUserUseCase,
    PasswordVerifier,
    TokenGenerator,
    TokenGeneratorRequest,
    TokenGeneratorResponse,
    TokenPurpose,
    TokenScheme,
)
from examples.tasker_primitive_obsession.src.domain.ports import UserRepository


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
        self._logger = logging.getLogger(__name__).getChild(self.__class__.__name__)

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
        self._logger.info("Executing user authentication with request: %s", request)
        user = await self._user_repository.find_by_email(request.email)

        if not user:
            raise ValueError("User not found")

        if not self._password_verifier.verify(request.password, user.password):
            raise ValueError("Invalid password")

        stringed_user_id = str(user.id)
        access_token = self._generate_access_token(stringed_user_id)
        refresh_token = self._generate_refresh_token(stringed_user_id)

        return AuthenticateUserResponse(
            access_token=access_token.token,
            access_token_expires_in=access_token.expires_in,
            refresh_token=refresh_token.token,
            refresh_token_expires_in=refresh_token.expires_in,
            token_scheme=TokenScheme.BEARER,
        )

    def _generate_access_token(self, user_id: str) -> TokenGeneratorResponse:
        """
        Generate an access token for the authenticated user.

        Args:
            user_id (str): The ID of the authenticated user.
        Returns:
            TokenGeneratorResponse: The response containing the access token and its
            expiration time.
        """
        request = TokenGeneratorRequest(user_id, TokenPurpose.ACCESS)
        self._logger.debug("Generating access token for user_id: %s", user_id)

        return self._access_token_generator.generate(request)

    def _generate_refresh_token(self, user_id: str) -> TokenGeneratorResponse:
        """
        Generate a refresh token for the authenticated user.

        Args:
            user_id (str): The ID of the authenticated user.
        Returns:
            TokenGeneratorResponse: The response containing the refresh token and its
            expiration time.
        """
        request = TokenGeneratorRequest(user_id, TokenPurpose.REFRESH)
        self._logger.debug("Generating refresh token for user_id: %s", user_id)

        return self._access_token_generator.generate(request)
