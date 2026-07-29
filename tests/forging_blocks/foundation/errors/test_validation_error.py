import pytest

from forging_blocks.foundation import (
    ErrorMessage,
    ValidationError,
    ValidationFailedError,
)


@pytest.mark.unit
class TestValidationError:
    def test_concrete_subclass_is_catchable_as_value_error(self) -> None:
        """ValidationFailedError is a ValueError via the mixin."""
        error = ValidationFailedError(ErrorMessage("Validation failed"))

        assert isinstance(error, ValueError)
        assert isinstance(error, ValidationError)

    def test_direct_instantiation_raises_typeerror(self) -> None:
        """ValidationError is abstract — direct instantiation must raise TypeError."""
        with pytest.raises(TypeError, match="ValidationError is abstract"):
            ValidationError(ErrorMessage("not allowed"))
