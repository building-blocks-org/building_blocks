import jwt

from examples.tasker_primitives.src.application.ports import (
    TokenValidator,
    TokenValidatorRequest,
    TokenValidatorResponse,
)


class JwtTokenValidator(TokenValidator):
    def __init__(self, secret_key: str, algorithm: str) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._jwt = jwt

    async def validate(self, request: TokenValidatorRequest) -> TokenValidatorResponse:
        try:
            payload = self._jwt.decode(
                request.token,
                self._secret_key,
                algorithms=[self._algorithm],
                options={
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_nbf": True,
                },
            )

            if payload.get("purpose") != request.purpose:
                return TokenValidatorResponse(
                    valid=False, reason="Token purpose does not match."
                )
            return TokenValidatorResponse(
                valid=True,
            )
        except jwt.InvalidSignatureError:
            return TokenValidatorResponse(
                valid=False, reason="Invalid token signature."
            )
        except jwt.ExpiredSignatureError:
            return TokenValidatorResponse(valid=False, reason="Token has expired.")
        except Exception as exc:
            return TokenValidatorResponse(valid=False, reason=str(exc))
