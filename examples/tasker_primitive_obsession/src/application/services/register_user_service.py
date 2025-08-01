import logging

from examples.tasker_primitive_obsession.src.application.ports import (
    PasswordHasher,
    RegisterUserRequest,
    RegisterUserResponse,
    RegisterUserUseCase,
)
from examples.tasker_primitive_obsession.src.domain.entities.user import User
from examples.tasker_primitive_obsession.src.domain.ports import UserRepository

from building_blocks.abstractions.result import Err

logger = logging.getLogger(__name__)


class RegisterUserService(RegisterUserUseCase):
    def __init__(
        self, user_repository: UserRepository, password_hasher: PasswordHasher
    ) -> None:
        """
        Initialize the RegisterUserService.
        This service implements the RegisterUserUseCase to handle user registration.
        """
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._logger = logger.getChild(self.__class__.__name__)

    async def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        """
        Execute the use case to register a new user.

        Args:
            request (RegisterUserRequest): The request containing user details.

        Returns:
            RegisterUserResponse: The response containing the registered user ID.
        """
        self._logger.debug("Executing user registration with request: %s", request)
        user = await self._create_user(request)

        await self._user_repository.save(user)

        return RegisterUserResponse(user_id=user.id.hex)

    async def _create_user(self, request: RegisterUserRequest) -> User:
        """
        Create a User entity from the request.

        Args:
            request (RegisterUserRequest): The request containing user details.

        Returns:
            User: The created User entity.
        """
        user_result = User.register(
            name=request.name,
            email=request.email,
            password=request.password,
            role=request.role,
        )

        if isinstance(user_result, Err):
            self._logger.error("Failed to create user: %s", user_result.error.message)
            raise user_result.error
        else:
            user = user_result.value
            encrypted_password = await self._password_hasher.hash(user.password)

            user.password = encrypted_password

            self._logger.info("User created successfully: %s", user)

            return user
