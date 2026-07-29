import pytest

from forging_blocks.foundation import (
    CombinedValidationErrors,
    ErrorMessage,
    FieldReference,
    ValidationFailedError,
    ValidationFieldErrors,
)


@pytest.mark.unit
class TestCombinedValidationErrors:
    def test_stores_and_iterates_field_errors(self) -> None:
        """CombinedValidationErrors aggregates field errors and supports iteration."""
        field_err1 = ValidationFieldErrors(
            FieldReference("username"),
            [ValidationFailedError(ErrorMessage("too short"))],
        )
        field_err2 = ValidationFieldErrors(
            FieldReference("email"),
            [ValidationFailedError(ErrorMessage("invalid format"))],
        )

        combined = CombinedValidationErrors([field_err1, field_err2])

        assert len(combined) == 2
        assert list(combined) == [field_err1, field_err2]
        assert combined.errors == (field_err1, field_err2)

    def test_catchable_as_value_error(self) -> None:
        """CombinedValidationErrors is a ValueError via the mixin."""
        combined = CombinedValidationErrors(
            [
                ValidationFieldErrors(
                    FieldReference("x"),
                    [ValidationFailedError(ErrorMessage("bad"))],
                )
            ]
        )
        assert isinstance(combined, ValueError)

    def test_str_includes_class_name_and_error_message(self) -> None:
        """str() includes the class name and each individual error."""
        combined = CombinedValidationErrors(
            [
                ValidationFieldErrors(
                    FieldReference("x"),
                    [ValidationFailedError(ErrorMessage("bad"))],
                )
            ]
        )

        result = str(combined)

        assert "CombinedValidationErrors" in result
        assert "bad" in result
