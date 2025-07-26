import bcrypt

from examples.tasker_primitives.src.application.ports import (
    PasswordHasher,
    PasswordVerifier,
)

Password = str
HashedPassword = str


class BCryptPasswordHasher(PasswordHasher[Password, HashedPassword]):
    """
    Implementation of PasswordHasher using bcrypt for hashing passwords.
    """

    async def hash(self, password: Password) -> HashedPassword:
        """
        Hash the given password using bcrypt.

        Args:
            password (Password): The password to hash.

        Returns:
            HashedPassword: The hashed password as bytes.
        """
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed.decode("utf-8")


class BCryptPasswordVerifier(PasswordVerifier[Password, HashedPassword]):
    async def verify(self, password: Password, hashed_password: HashedPassword) -> bool:
        """
        Verify that the given password matches the encrypted password.

        Args:
            password (Password): The plain password to check.
            encrypted_password (HashedPassword): The hashed password as bytes.

        Returns:
            bool: True if match, False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
