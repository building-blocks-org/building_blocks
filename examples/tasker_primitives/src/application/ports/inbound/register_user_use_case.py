from abc import abstractmethod
from dataclasses import dataclass

from building_blocks.application.ports.inbound.use_case import AsyncUseCase as UseCase


@dataclass(frozen=True)
class RegisterUserRequest:
    name: str
    email: str
    password: str
    role: str


@dataclass(frozen=True)
class RegisterUserResponse:
    user_id: str


class RegisterUserUseCase(UseCase[RegisterUserRequest, RegisterUserResponse]):
    @abstractmethod
    async def execute(self, request: RegisterUserRequest) -> RegisterUserResponse:
        """
        Execute the use case to create a new task.

        Args:
            request (RegisterUserRequest): The request containing task details.

        Returns:
            RegisterUserResponse: The response containing the created task ID.
        """
        pass
