class UserEmailAlreadyExistsError(Exception):
    """Exception raised when a user with the same email already exists."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists.")

    def __str__(self):
        return f"UserEmailAlreadyExistsError: {self.email}"
