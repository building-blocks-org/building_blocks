from building_blocks.domain.domain_error import DomainError


class TaskStatusTransitionError(DomainError):
    """Exception raised when a task status transition is invalid."""

    def __init__(self, message: str = "Invalid task status transition."):
        super().__init__(message)
        self.message = message
