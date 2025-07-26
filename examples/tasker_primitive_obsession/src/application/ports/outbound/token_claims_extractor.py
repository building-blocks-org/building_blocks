from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from examples.tasker_primitive_obsession.src.application.ports import (
    TokenClaims,
)


@dataclass(frozen=True)
class TokenClaimsExtractorRequest:
    """
    Represents a request to extract claims from a token.
    This class is used to encapsulate the token from which claims need to be extracted.
    """

    token: str


@dataclass(frozen=True)
class TokenClaimsExtractorResponse:
    """
    Represents the response from extracting claims from a token.
    This class contains the extracted claims, an optional error message, and a flags
    indicating whether the extraction was successful.
    """

    claims: Optional[TokenClaims] = None
    error: Optional[str] = None


class TokenClaimsExtractor(ABC):
    @abstractmethod
    def extract(
        self, request: TokenClaimsExtractorRequest
    ) -> TokenClaimsExtractorResponse:
        """
        Extract claims from a token.

        :param request: The request containing the token from which claims need to be
        extracted.

        :return: A TokenClaimsExtractorResponse containing the extracted claims or and
        error message if extraction fails.
        """
        pass
