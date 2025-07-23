from examples.tasker_primitives.src.application.ports import (
    TokenGenerator,
    TokenGeneratorRequest,
    TokenGeneratorResponse,
)


class JwtTokenGenerator(TokenGenerator):
    def __init__(self, expires_in: int) -> None:
        self._expires_in = expires_in

    def generate(self, input: TokenGeneratorRequest) -> TokenGeneratorResponse:
        return TokenGeneratorResponse(
            token=f"jwt_token_for_{input.user_id}_for_{input.purpose}",
            expires_in=self._expires_in,
        )


jwt_access_token_generator = JwtTokenGenerator(3600)
jwt_refresh_token_generator = JwtTokenGenerator(604800)
