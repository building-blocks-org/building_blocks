import pytest

from forging_blocks.application.ports.inbound.validation_port import ValidationPort
from forging_blocks.foundation.errors import RuleViolated, RuleViolationError
from forging_blocks.foundation.errors.core import ErrorMessage


@pytest.mark.unit
class TestValidationPort:
    async def test_when_concrete_implementation_then_returns_command_errors(self) -> None:
        class StrictValidator(ValidationPort):
            async def validate_command(self, command: object) -> list[RuleViolationError]:
                return [RuleViolated(ErrorMessage("invalid"))]

            async def validate_query(self, query: object) -> list[RuleViolationError]:
                del query
                return []

        service = StrictValidator()
        errors = await service.validate_command("data")

        assert len(errors) == 1
        assert str(errors[0]) == "RuleViolated: invalid"

    async def test_when_valid_query_then_returns_empty(self) -> None:
        class PermissiveValidator(ValidationPort):
            async def validate_command(self, command: object) -> list[RuleViolationError]:
                del command
                return []

            async def validate_query(self, query: object) -> list[RuleViolationError]:
                del query
                return []

        service = PermissiveValidator()
        errors = await service.validate_query("any")

        assert errors == []
