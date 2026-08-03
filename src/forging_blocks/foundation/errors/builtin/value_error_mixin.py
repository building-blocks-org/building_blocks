"""Make forging-blocks errors catchable as Python built-in ``ValueError``.

Defines ``ValueErrorMixin``, a mixin class extending Python's built-in
``ValueError``. When listed before ``Error[...]`` in a class's bases, it
adjusts the MRO so that ``isinstance(error, ValueError)`` returns ``True``.

Attach ``ValueErrorMixin`` to errors representing invalid input, bad
arguments, and precondition failures.
"""


class ValueErrorMixin(ValueError):
    """Mixin — attach before ``Error[...]`` in MRO to make errors ``isinstance(ValueError)``.

    Example:
        ```python
        from forging_blocks.foundation.errors import Error, ErrorMessage


        class InvalidInputError(ValueErrorMixin, Error[str]):
            pass  # This error represents invalid input


        err = InvalidInputError(ErrorMessage("Bad input"))
        assert isinstance(err, ValueError)
        ```
    """
