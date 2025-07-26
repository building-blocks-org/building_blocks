import logging

from examples.tasker_primitive_obsession.src.application.ports import (
    TokenValidator,
    TokenValidatorRequest,
    ValidateTokenRequest,
    ValidateTokenResponse,
    ValidateTokenUseCase,
)


class ValidateTokenService(ValidateTokenUseCase):
    def __init__(self, token_validator: TokenValidator) -> None:
        self._token_validator = token_validator
        self._logger = logging.getLogger(__name__).getChild(self.__class__.__name__)

    async def execute(self, request: ValidateTokenRequest) -> ValidateTokenResponse:
        self._logger.info("Validating token: %s", request.token)
        validator_request = TokenValidatorRequest(
            token=request.token, purpose=request.purpose
        )
        validator_response = await self._token_validator.validate(validator_request)

        if not validator_response.valid:
            self._logger.warning("Invalid token: %s", request.token)

            return ValidateTokenResponse(valid=False, reason="Invalid token request")

        self._logger.info("Token is valid: %s")

        return ValidateTokenResponse(valid=True, claims=None, reason=None)
