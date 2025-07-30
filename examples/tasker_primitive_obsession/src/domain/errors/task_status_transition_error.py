from typing import Dict, Optional

from building_blocks.domain.errors import DomainRuleViolationError


class TaskStatusTransitionError(DomainRuleViolationError):
    """Exception raised when a task status transition is invalid."""

    def __init__(
        self,
        message: str = "Invalid task status transition.",
        from_status: Optional[str] = None,
        to_status: Optional[str] = None,
        context: Optional[Dict] = None,
    ):
        extra_context = context or {}
        if from_status:
            extra_context["from_status"] = from_status
        if to_status:
            extra_context["to_status"] = to_status

        super().__init__(
            message=message,
            context=extra_context,
        )
        self.message = message

    def __str__(self):
        base = self.message
        if self.rule:
            base = f"[{self.rule}] {base}"
        if self.context:
            base = f"{base} | Context: {self.context}"
        return base
