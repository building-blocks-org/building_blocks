from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenValidatorRequest:
    token: str
    purpose: str


@dataclass(frozen=True)
class TokenValidatorResponse:
    valid: bool
    reason: str = ""


class TokenValidator(ABC):
    @abstractmethod
    async def validate(self, request: TokenValidatorRequest) -> TokenValidatorResponse:
        """
        Validate the provided token for the given purpose.
        """
        pass
