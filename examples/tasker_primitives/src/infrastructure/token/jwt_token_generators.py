from datetime import datetime, timedelta, timezone

import jwt

from examples.tasker_primitives.src.application.ports import (
    TokenGenerator,
    TokenGeneratorRequest,
    TokenGeneratorResponse,
)
from examples.tasker_primitives.src.infrastructure.config import get_app_settings


class JwtTokenGenerator(TokenGenerator):
    def __init__(
        self, expires_in: int, secret_key: str, algorithm: str = "HS256"
    ) -> None:
        self._expires_in = expires_in
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._jwt = jwt

    def generate(self, request: TokenGeneratorRequest) -> TokenGeneratorResponse:
        expires_at = datetime.now(tz=timezone.utc) + timedelta(seconds=self._expires_in)

        try:
            token = self._jwt.encode(
                {
                    "user_id": request.user_id,
                    "purpose": request.purpose,
                    "exp": int(expires_at.timestamp()),
                },
                self._secret_key,
                algorithm=self._algorithm,
            )

        except Exception as exc:
            raise RuntimeError("Token generation failed") from exc

        return TokenGeneratorResponse(
            token=token,
            expires_in=self._expires_in,
        )


app_settings = get_app_settings()

jwt_access_token_generator = JwtTokenGenerator(
    app_settings.access_token_expires_in, secret_key=app_settings.secret_key
)
jwt_refresh_token_generator = JwtTokenGenerator(
    app_settings.refresh_token_expires_in, secret_key=app_settings.secret_key
)
