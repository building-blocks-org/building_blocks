"""Error raised when ``None`` is passed where a non-null value is required.

Defines ``NoneNotAllowedError``, used by validation guards and the
``NoneNotAllowed`` predicate to enforce non-null constraints on method
parameters and field values.  Extends ``ValueErrorMixin`` (catchable as
``ValueError``) and ``Error[str]``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin


class NoneNotAllowedError(ValueErrorMixin, Error[str]):
    """Error indicating that a None value was provided where it is not allowed.

    Example:
        ```python
        error = NoneNotAllowedError(ErrorMessage("Value cannot be None"))
        raise error
        ```

    """
