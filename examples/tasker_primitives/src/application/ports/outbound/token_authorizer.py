from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenAuthorizerRequest:
    token: str


@dataclass(frozen=True)
class TokenAuthorizerResponse:
    authorized: bool


class TokenAuthorizer(ABC):
    @abstractmethod
    def authorize(self, request: TokenAuthorizerRequest) -> TokenAuthorizerResponse:
        """
        Check a token if it is authorized.

        :param request: The input containing the token to validate.
        :return: A TokenAuthorizerOutput indicating whether the token is authorized.
        """
        pass
