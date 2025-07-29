from fastapi import Request
from fastapi.responses import JSONResponse

from building_blocks.domain.domain_error import DomainError

ERROR_STATUS_MAP = {
    DomainError: 400,  # Bad Request
}


def get_status_code(exc: Exception) -> int:
    """
    Get the HTTP status code for a given exception.
    """
    for error_type, status_code in ERROR_STATUS_MAP.items():
        if isinstance(exc, error_type):
            return status_code
    return 500


def generic_error_handler(_: Request, exc: Exception):
    status_code = get_status_code(exc)

    return JSONResponse(
        status_code=status_code,
        content={
            "error": type(exc).__name__,
            "message": str(exc),
            "details": getattr(exc, "details", None),
        },
    )
