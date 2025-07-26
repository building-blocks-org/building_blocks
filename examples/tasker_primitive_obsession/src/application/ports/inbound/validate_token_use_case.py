from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ValidateTokenRequest:
    token: str
    purpose: str


@dataclass(frozen=True)
class ValidateTokenResponse:
    valid: bool
    claims: Optional[Dict] = None
    reason: Optional[str] = None


class ValidateTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, request: ValidateTokenRequest) -> ValidateTokenResponse:
        """
        Validate a token based on the provided request.

        :param request: The input containing the token and purpose.
        :return: A ValidateTokenResponse indicating whether the token is valid.
        """
        pass
