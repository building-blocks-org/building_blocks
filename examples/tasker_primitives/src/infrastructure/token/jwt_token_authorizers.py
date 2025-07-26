import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from examples.tasker_primitives.src.application.ports import (
    TokenAlgorithm,
    TokenAuthorizer,
    TokenAuthorizerRequest,
    TokenAuthorizerResponse,
    TokenClaims,
)
from examples.tasker_primitives.src.infrastructure.config import get_app_settings


class JwtTokenAuthorizer(TokenAuthorizer):
    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._jwt = jwt

    async def authorize(
        self, request: TokenAuthorizerRequest
    ) -> TokenAuthorizerResponse:
        try:
            payload = self._jwt.decode(
                request.token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
            claims = TokenClaims(
                user_id=payload["sub"],
                expires_at=payload["exp"],
                email=payload["email"],
            )

            return TokenAuthorizerResponse(authorized=True, claims=claims)
        except ExpiredSignatureError:
            return TokenAuthorizerResponse(authorized=False, reason="Token expired")
        except (InvalidTokenError, KeyError):
            return TokenAuthorizerResponse(
                authorized=False, reason="Invalid token or missing claims."
            )


app_settings = get_app_settings()

jwt_access_token_authorizer = JwtTokenAuthorizer(
    secret_key=app_settings.secret_key,
    algorithm=TokenAlgorithm.HS256,
)
jwt_refresh_token_authorizer = JwtTokenAuthorizer(
    secret_key=app_settings.secret_key,
    algorithm=TokenAlgorithm.HS256,
)
