"""Verify ValueErrorMixin makes forging-blocks errors catchable as ValueError."""

import pytest

from forging_blocks.foundation.errors import (
    CombinedValidationErrors,
    ConfigurationError,
    Error,
    ErrorMessage,
    NoneNotAllowedError,
    NonHashableValueError,
    ValidationFailedError,
    ValueErrorMixin,
)

_VALID_MSG = ErrorMessage("test error")


class TestValueErrorMixin:
    """Errors with ValueErrorMixin are catchable as ValueError."""

    @pytest.mark.parametrize(
        "error_factory",
        [
            pytest.param(lambda: ValidationFailedError(_VALID_MSG), id="ValidationFailedError"),
            pytest.param(
                lambda: CombinedValidationErrors([]),
                id="CombinedValidationErrors",
            ),
            pytest.param(
                lambda: NoneNotAllowedError(_VALID_MSG),
                id="NoneNotAllowedError",
            ),
            pytest.param(
                lambda: NonHashableValueError("FakeType"),
                id="NonHashableValueError",
            ),
            pytest.param(
                lambda: ConfigurationError("broken config"),
                id="ConfigurationError",
            ),
        ],
    )
    def test_isinstance_value_error(self, error_factory: object) -> None:
        """Errors that inherit ValueErrorMixin are isinstance(ValueError)."""
        error = error_factory()  # type: ignore[reportUnknownVariableType]
        assert isinstance(error, ValueError)
        assert isinstance(error, Exception)

    def test_mro_mixin_before_base_error(self) -> None:
        """ValidationError MRO: ValueErrorMixin comes before Error[...]."""
        from forging_blocks.foundation.errors.base.validation_error import (
            ValidationError,
        )

        mro = ValidationError.__mro__
        mixin_idx = mro.index(ValueErrorMixin)
        error_idx = mro.index(Error)
        assert mixin_idx < error_idx, (
            f"ValueErrorMixin (idx {mixin_idx}) must precede Error (idx {error_idx}) in MRO"
        )

    def test_caught_as_value_error(self) -> None:
        """ValidationFailedError is caught by except ValueError."""
        caught = False
        try:
            raise ValidationFailedError(_VALID_MSG)
        except ValueError:
            caught = True
        except Exception:
            pass
        assert caught

    def test_caught_as_exception(self) -> None:
        """ValidationFailedError is caught by except Exception."""
        caught = False
        try:
            raise ValidationFailedError(_VALID_MSG)
        except Exception:
            caught = True
        assert caught

    def test_bypasses_runtime_error(self) -> None:
        """ValidationFailedError is NOT caught by RuntimeError."""
        caught_by_runtime = False
        caught_by_value = False
        try:
            raise ValidationFailedError(_VALID_MSG)
        except RuntimeError:
            caught_by_runtime = True
        except ValueError:
            caught_by_value = True
        assert not caught_by_runtime
        assert caught_by_value

    def test_root_error_is_not_value_error(self) -> None:
        """Root Error class does NOT extend ValueError."""
        assert not issubclass(Error, ValueError)

    def test_root_error_is_not_runtime_error(self) -> None:
        """Root Error class does NOT extend RuntimeError."""
        assert not issubclass(Error, RuntimeError)

    def test_root_error_is_exception(self) -> None:
        """Root Error class does extend Exception."""
        assert issubclass(Error, Exception)
