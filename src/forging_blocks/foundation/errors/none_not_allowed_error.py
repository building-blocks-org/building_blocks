"""Error indicating that a None value was provided where it is not allowed."""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin


class NoneNotAllowedError(ValueErrorMixin, Error[str]):
    """Error indicating that a None value was provided where it is not allowed."""
