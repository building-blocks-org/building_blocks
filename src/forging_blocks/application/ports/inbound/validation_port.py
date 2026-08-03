"""Inbound port for domain command and query validation.

Responsibilities:
    - Validate commands and queries against business rules.
    - Return structured validation errors.

Non-Responsibilities:
    - Execute commands or queries.
    - Implement business logic directly.
"""

from abc import abstractmethod

from forging_blocks.domain.messages.command import Command
from forging_blocks.domain.messages.query import Query
from forging_blocks.foundation.errors.base.rule_violation_error import RuleViolationError
from forging_blocks.foundation.ports import InboundPort


class ValidationPort[CommandPayloadType, QueryPayloadType](InboundPort):
    """Inbound port for domain command and query validation.

    Responsibilities:
        - Inspect command and query payloads for rule violations.
        - Return a list of ``RuleViolationError`` instances.

    Non-Responsibilities:
        - Enforce authorization (handled by ``AuthorizationPort``).
        - Modify command or query state.

    Example:
        ```python
        from forging_blocks.domain.messages.command import Command

        class CreateOrderCommand:
            product_id: str
            quantity: int

        class CreateOrderValidator(ValidationPort[CreateOrderCommand, object]):
            async def validate_command(self, command: Command[CreateOrderCommand]) -> list[RuleViolationError]:
                return []

            ...
        ```
    """

    @abstractmethod
    async def validate_command(
        self, command: Command[CommandPayloadType]
    ) -> list[RuleViolationError]:
        """Validate a domain command."""
        ...

    @abstractmethod
    async def validate_query(self, query: Query[QueryPayloadType]) -> list[RuleViolationError]:
        """Validate a domain query."""
        ...
