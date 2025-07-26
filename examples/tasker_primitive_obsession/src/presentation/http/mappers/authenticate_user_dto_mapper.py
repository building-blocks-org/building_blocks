from examples.tasker_primitive_obsession.src.application.ports import (
    AuthenticateUserRequest,
    AuthenticateUserResponse,
)
from examples.tasker_primitive_obsession.src.presentation.http.requests import (
    AuthenticateUserHttpRequest,
)
from examples.tasker_primitive_obsession.src.presentation.http.responses import (
    AuthenticateUserHttpResponse,
)


class AuthenticateUserDtoMapper:
    @staticmethod
    def from_http_request(
        request: AuthenticateUserHttpRequest,
    ) -> AuthenticateUserRequest:
        """
        Maps the HTTP request to a service request dictionary.

        Args:
            request: The HTTP request containing user credentials.

        Returns:
            dict: A dictionary containing the user credentials.
        """
        return AuthenticateUserRequest(email=request.email, password=request.password)

    @staticmethod
    def to_http_response(
        response: AuthenticateUserResponse,
    ) -> AuthenticateUserHttpResponse:
        """
        Maps the service response to an HTTP response.

        Args:
            response: The service response containing access token, refresh token, their
            expiration times and token scheme.



        Returns:
            AuthenticateUserHttpResponse: An HTTP response containing the access token,
            refresh token, their expiration times and token scheme.
        """
        return AuthenticateUserHttpResponse(
            access_token=response.access_token,
            access_token_expires_in=response.access_token_expires_in,
            refresh_token=response.refresh_token,
            refresh_token_expires_in=response.refresh_token_expires_in,
            token_scheme=response.token_scheme,
        )
