import pytest

from forging_blocks.foundation import (
    ErrorMessage,
    RuleViolatedError,
    RuleViolationError,
)


@pytest.mark.unit
class TestRuleViolationError:
    def test_concrete_subclass_is_catchable_as_runtime_error(self) -> None:
        """RuleViolatedError is a RuntimeError via the mixin."""
        error = RuleViolatedError(ErrorMessage("Test rule violation"))

        assert isinstance(error, RuntimeError)
        assert isinstance(error, RuleViolationError)

    def test_direct_instantiation_raises_typeerror(self) -> None:
        """RuleViolationError is abstract — direct instantiation must raise TypeError."""
        with pytest.raises(TypeError, match="RuleViolationError is abstract"):
            RuleViolationError(ErrorMessage("not allowed"))
