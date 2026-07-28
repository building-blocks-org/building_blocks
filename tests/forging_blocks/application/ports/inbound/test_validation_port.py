import pytest
from tests.fixtures.simple_fake_command import SimpleFakeCommand
from tests.fixtures.simple_fake_query import SimpleFakeQuery

from forging_blocks.application.ports.inbound.validation_port import ValidationPort
from forging_blocks.domain.messages.command import Command
from forging_blocks.domain.messages.query import Query
from forging_blocks.foundation.errors import RuleViolatedError, RuleViolationError
from forging_blocks.foundation.errors.core import ErrorMessage


@pytest.mark.unit
class TestValidationPort:
    async def test_when_concrete_implementation_then_returns_command_errors(self) -> None:
        class StrictValidator(ValidationPort[dict[str, object], dict[str, object]]):
            async def validate_command(
                self, command: Command[dict[str, object]]
            ) -> list[RuleViolationError]:
                return [RuleViolatedError(ErrorMessage("invalid"))]

            async def validate_query(
                self, query: Query[dict[str, object]]
            ) -> list[RuleViolationError]:
                del query
                return []

        service = StrictValidator()
        errors = await service.validate_command(SimpleFakeCommand("test"))

        assert len(errors) == 1
        assert str(errors[0]) == "RuleViolatedError: invalid"

    async def test_when_valid_query_then_returns_empty(self) -> None:
        class PermissiveValidator(ValidationPort[dict[str, object], dict[str, object]]):
            async def validate_command(
                self, command: Command[dict[str, object]]
            ) -> list[RuleViolationError]:
                del command
                return []

            async def validate_query(
                self, query: Query[dict[str, object]]
            ) -> list[RuleViolationError]:
                del query
                return []

        service = PermissiveValidator()
        errors = await service.validate_query(SimpleFakeQuery("test"))

        assert errors == []
