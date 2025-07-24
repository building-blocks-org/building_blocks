from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


class TokenGeneratorPurpose:
    ACCESS = "access"
    REFRESH = "refresh"


@dataclass(frozen=True)
class TokenGeneratorRequest:
    user_id: str
    purpose: str


@dataclass(frozen=True)
class TokenGeneratorResponse:
    token: str
    expires_in: int


class TokenGenerator(ABC):
    @abstractmethod
    def generate(self, input: TokenGeneratorRequest) -> TokenGeneratorResponse:
        """
        Generate a token based on the provided request.

        Args:
            input (TokenGeneratorRequest): The request containing user ID and purpose.

        Returns:
            TokenGeneratorResponse: The response containing the generated token and its
            expiration time.
        """
        pass
