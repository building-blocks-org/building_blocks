import jwt

from examples.tasker_primitives.src.application.ports import (
    TokenClaimsExtractor,
    TokenClaimsExtractorRequest,
    TokenClaimsExtractorResponse,
)


class JwtTokenClaimsExtractor(TokenClaimsExtractor):
    """
    Extracts token claims from a JWT token.
    """

    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        """
        Initializes the JWT token claims extractor with a secret key and algorithm.

        :param secret_key: The secret key used to decode the JWT token.
        :param algorithm: The algorithm used for decoding the JWT token.
        """
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._jwt = jwt

    def extract(
        self, request: TokenClaimsExtractorRequest
    ) -> TokenClaimsExtractorResponse:
        """
        Extracts claims from the provided JWT token.
        :param request: The request containing the JWT token to extract claims from.

        :return: A response containing the extracted claims or an error message.
        """
        try:
            payload = self._jwt.decode(
                request.token,
                self._secret_key,
                algorithms=[self._algorithm],
                options={"verify_exp": False, "verify_nbf": False},
            )
            claims = {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "roles": payload.get("roles"),
                "expires_at": payload.get("exp"),
            }
            return TokenClaimsExtractorResponse(claims=claims)
        except jwt.ExpiredSignatureError:
            return TokenClaimsExtractorResponse(error="Token expired")
        except jwt.InvalidTokenError:
            return TokenClaimsExtractorResponse(error="Invalid token")
        except Exception as exc:
            return TokenClaimsExtractorResponse(error=f"Unexpected error: {str(exc)}")
