from examples.tasker_primitive_obsession.src.application.ports import (
    TokenAlgorithm,
    ValidateTokenUseCase,
)
from examples.tasker_primitive_obsession.src.application.services import (
    ValidateTokenService,
)
from examples.tasker_primitive_obsession.src.infrastructure.config import (
    get_app_settings,
)
from examples.tasker_primitive_obsession.src.infrastructure.token import (
    JwtTokenValidator,
)

settings = get_app_settings()


def get_validate_token_use_case() -> ValidateTokenUseCase:
    token_validator = JwtTokenValidator(
        secret_key=settings.secret_key, algorithm=TokenAlgorithm.HS256
    )

    return ValidateTokenService(token_validator)
