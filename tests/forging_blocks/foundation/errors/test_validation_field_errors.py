import pytest

from forging_blocks.foundation import (
    ErrorMessage,
    FieldReference,
    RuleViolatedError,
    ValidationFailedError,
    ValidationFieldErrors,
)


@pytest.mark.unit
class TestValidationFieldErrors:
    def test_stores_field_and_iterates_errors(self) -> None:
        """ValidationFieldErrors exposes the field and supports iteration."""
        error = ValidationFailedError(ErrorMessage("Too short"))
        field = FieldReference("username")

        field_errors = ValidationFieldErrors(field, [error])

        assert field_errors.field is field
        assert len(field_errors) == 1
        assert list(field_errors) == [error]
        assert field_errors.errors == (error,)

    def test_catchable_as_value_error(self) -> None:
        """ValidationFieldErrors is a ValueError via the mixin."""
        field_errors = ValidationFieldErrors(
            FieldReference("username"),
            [ValidationFailedError(ErrorMessage("failed"))],
        )
        assert isinstance(field_errors, ValueError)

    def test_empty_errors_raises_rule_violated(self) -> None:
        """FieldErrors must contain at least one error."""
        with pytest.raises(RuleViolatedError, match="at least one error"):
            ValidationFieldErrors(FieldReference("username"), [])

    def test_falsy_field_reference_raises_rule_violated(self) -> None:
        """FieldErrors requires a non-empty field reference."""
        with pytest.raises(RuleViolatedError, match="at least one error"):
            ValidationFieldErrors(FieldReference(""), [ValidationFailedError(ErrorMessage("err"))])

    def test_str_includes_field_name(self) -> None:
        """The string representation includes the field name."""
        field_errors = ValidationFieldErrors(
            FieldReference("email"),
            [ValidationFailedError(ErrorMessage("invalid format"))],
        )
        assert "email" in str(field_errors)
