"""
Domain Use Case port for pure domain operations.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TRequest = TypeVar("TRequest")
TResponse = TypeVar("TResponse")


class DomainUseCase(ABC, Generic[TRequest, TResponse]):
    """
    Synchronous version of DomainUseCase.

    Use this when:
    - Your domain operations don't require async/await
    - You're working in a synchronous context
    - You want to avoid async overhead for simple operations
    """

    @abstractmethod
    def execute(self, request: TRequest) -> TResponse:
        """
        Execute the domain use case synchronously.

        Args:
            request: The domain operation request/input

        Returns:
            The domain operation response/output

        Raises:
            DomainException: When domain rules are violated
        """
        pass
