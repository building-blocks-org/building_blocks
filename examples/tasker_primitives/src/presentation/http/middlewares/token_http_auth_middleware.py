import logging

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from examples.tasker_primitives.src.application.ports import (
    TokenScheme,
    ValidateTokenRequest,
    ValidateTokenUseCase,
)


class TokenHttpAuthMiddleware(BaseHTTPMiddleware):
    _public_routes = {
        ("/users", "POST"),
        ("/users/sign_in", "POST"),
        ("/users/refresh", "POST"),
    }

    def __init__(self, app: ASGIApp, use_case: ValidateTokenUseCase) -> None:
        super().__init__(app)
        self._use_case = use_case
        self._logger = logging.getLogger(__name__).getChild(self.__class__.__name__)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        self._logger.info("Processing request: %s %s", request.method, request.url.path)

        if self._is_public_endpoint(request):
            self._logger.info(
                "Public endpoint accessed: %s %s", request.method, request.url.path
            )
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        self._logger.debug("Authorization header: %s", auth_header)

        if self._is_token_scheme_invalid(auth_header):
            self._logger.warning("Invalid Authorization header format: %s", auth_header)
            return JSONResponse(
                {"details": "Missing or malformed Authorization header"},
                status_code=401,
            )

        token = auth_header.split()[1]
        use_case_request = ValidateTokenRequest(token=token, purpose="access")
        use_case_response = await self._use_case.execute(use_case_request)

        if not use_case_response.valid:
            self._logger.warning(
                "Invalid token for request: %s %s, reason: %s",
                request.method,
                request.url.path,
                use_case_response.reason or "Unknown reason",
            )
            return JSONResponse(
                {"details": use_case_response.reason or "Unauthorized access"},
                status_code=401,
            )

        request.state.claims = use_case_response.claims
        response = await call_next(request)

        self._logger.info(
            "Request processed successfully: %s %s", request.method, request.url.path
        )

        return response

    def _is_token_scheme_invalid(self, auth_header: str) -> bool:
        """
        Return True if the Authorization header is missing or not a valid Bearer token.

        auth_header: The value of the Authorization header.
        Returns True if the header is invalid, False if it is valid.

        It must be in the format "Bearer <token>".
        """
        parts = auth_header.split()

        if len(parts) != 2:
            return True
        return parts[0].lower() != TokenScheme.BEARER.lower()

    def _is_public_endpoint(self, request: Request) -> bool:
        """
        Check if the endpoint is public and does not require authentication.
        """
        return (request.url.path, request.method) in self._public_routes
