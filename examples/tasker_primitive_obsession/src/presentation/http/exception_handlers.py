from fastapi import Request
from fastapi.responses import JSONResponse

from building_blocks.domain.errors import (
    DomainError,
    DomainRuleViolationError,
    DomainValidationError,
)

ERROR_STATUS_MAP = {
    DomainValidationError: 422,
    DomainRuleViolationError: 409,
    DomainError: 400,
}


def get_status_code(exc: Exception) -> int:
    """
    Get the HTTP status code for a given exception.
    """
    for error_type, status_code in ERROR_STATUS_MAP.items():
        if isinstance(exc, error_type):
            return status_code
    return 500


def domain_error_handler(_: Request, exc: DomainError):
    status_code = get_status_code(exc)
    details = getattr(exc, "context", None) or getattr(exc, "details", None)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": type(exc).__name__,
            "message": exc.message if hasattr(exc, "message") else str(exc),
            "details": details,
        },
    )


def fallback_error_handler(_: Request, exc: Exception):
    """
    Fallback error handler for unhandled exceptions.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred.",
            "details": str(exc),
        },
    )
