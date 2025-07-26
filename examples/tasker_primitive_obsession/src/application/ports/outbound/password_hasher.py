from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TPassword = TypeVar("TPassword")
THashedPassword = TypeVar("THashedPassword")


class PasswordHasher(ABC, Generic[TPassword, THashedPassword]):
    """
    Password encrypter interface for encrypting passwords.

    This interface defines the contract for encrypting passwords.
    It can be implemented by various encryption services.
    """

    @abstractmethod
    async def hash(self, password: TPassword) -> THashedPassword:
        """
        Encrypt the given password.

        Args:
            password (TPassword): The password to be encrypted.

        Returns:
            THashedPassword: The hashed password.
        """
        pass
