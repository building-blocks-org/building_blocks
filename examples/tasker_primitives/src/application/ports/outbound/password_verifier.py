from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TPassword = TypeVar("TPassword")
THashedPassword = TypeVar("THashedPassword")


class PasswordVerifier(ABC, Generic[TPassword, THashedPassword]):
    @abstractmethod
    async def verify(
        self, password: TPassword, encrypted_password: THashedPassword
    ) -> bool:
        """
        Verify if the provided password matches the encrypted password.

        Args:
            password (TPassword): The plain text password to verify.
            encrypted_password (THashedPassword): The encrypted password to compare
            against.

        Returns:
            bool: True if the passwords match, False otherwise.
        """
        pass
