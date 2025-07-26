from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from examples.tasker_primitive_obsession.src.application.ports import (
    TokenClaims,
)


@dataclass(frozen=True)
class TokenAuthorizerRequest:
    token: str


@dataclass(frozen=True)
class TokenAuthorizerResponse:
    authorized: bool
    claims: Optional[TokenClaims] = None
    reason: Optional[str] = None


class TokenAuthorizer(ABC):
    @abstractmethod
    async def authorize(
        self, request: TokenAuthorizerRequest
    ) -> TokenAuthorizerResponse:
        """
        Check a token if it is authorized.

        :param request: The input containing the token to validate.
        :return: A TokenAuthorizerOutput indicating whether the token is authorized.
        """
        pass
