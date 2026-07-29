"""Verify RuntimeErrorMixin makes forging-blocks errors catchable as RuntimeError."""

import pytest

from forging_blocks.foundation.errors import (
    ArchitectureError,
    CantModifyImmutableAttributeError,
    CombinedRuleViolationErrors,
    Error,
    ErrorMessage,
    ResultAccessError,
    RuleViolatedError,
    RuntimeErrorMixin,
)

_VALID_MSG = ErrorMessage("test error")


class TestRuntimeErrorMixin:
    """Errors with RuntimeErrorMixin are catchable as RuntimeError."""

    @pytest.mark.parametrize(
        "error_factory",
        [
            pytest.param(lambda: RuleViolatedError(_VALID_MSG), id="RuleViolatedError"),
            pytest.param(lambda: ArchitectureError("bad arch"), id="ArchitectureError"),
            pytest.param(
                lambda: CombinedRuleViolationErrors([]),
                id="CombinedRuleViolationErrors",
            ),
            pytest.param(
                lambda: CantModifyImmutableAttributeError("FakeClass", "fake_attr"),
                id="CantModifyImmutableAttributeError",
            ),
            pytest.param(
                lambda: ResultAccessError(),
                id="ResultAccessError",
            ),
        ],
    )
    def test_isinstance_runtime_error(self, error_factory: object) -> None:
        """Errors that inherit RuntimeErrorMixin are isinstance(RuntimeError)."""
        error = error_factory()  # type: ignore[reportUnknownVariableType]
        assert isinstance(error, RuntimeError)
        assert isinstance(error, Exception)

    def test_mro_mixin_before_base_error(self) -> None:
        """RuleViolationError MRO: RuntimeErrorMixin comes before Error[...]."""
        from forging_blocks.foundation.errors.base.rule_violation_error import (
            RuleViolationError,
        )

        mro = RuleViolationError.__mro__
        mixin_idx = mro.index(RuntimeErrorMixin)
        error_idx = mro.index(Error)
        assert mixin_idx < error_idx, (
            f"RuntimeErrorMixin (idx {mixin_idx}) must precede Error (idx {error_idx}) in MRO"
        )

    def test_caught_as_runtime_error(self) -> None:
        """RuleViolatedError is caught by except RuntimeError."""
        caught = False
        try:
            raise RuleViolatedError(_VALID_MSG)
        except RuntimeError:
            caught = True
        except Exception:
            pass
        assert caught
