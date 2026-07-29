import pytest

from forging_blocks.foundation import (
    CombinedRuleViolationErrors,
    ErrorMessage,
    RuleViolatedError,
)


@pytest.mark.unit
class TestCombinedRuleViolationErrors:
    def test_stores_and_iterates_errors(self) -> None:
        """CombinedRuleViolationErrors aggregates errors and supports iteration."""
        err1 = RuleViolatedError(ErrorMessage("Rule A violated"))
        err2 = RuleViolatedError(ErrorMessage("Rule B violated"))

        combined = CombinedRuleViolationErrors([err1, err2])

        assert len(combined) == 2
        assert list(combined) == [err1, err2]
        assert combined.errors == (err1, err2)

    def test_catchable_as_runtime_error(self) -> None:
        """CombinedRuleViolationErrors is a RuntimeError via the mixin."""
        combined = CombinedRuleViolationErrors([RuleViolatedError(ErrorMessage("failed"))])
        assert isinstance(combined, RuntimeError)

    def test_str_includes_class_name_and_error_message(self) -> None:
        """str() includes the class name and each individual error."""
        err = RuleViolatedError(ErrorMessage("Rule A violated"))
        combined = CombinedRuleViolationErrors([err])

        result = str(combined)

        assert "CombinedRuleViolationErrors" in result
        assert "Rule A violated" in result
