"""Mix-in for making forging-blocks errors catchable as built-in ``RuntimeError``.

Defines ``RuntimeErrorMixin``, which extends Python's built-in ``RuntimeError``.
When listed before ``Error[...]`` in a class's bases, the mix-in ensures
``isinstance(error, RuntimeError)`` returns ``True`` for that error and its
subclasses.  Attach it to errors representing state violations, broken
invariants, and operational failures where ``except RuntimeError`` should apply.
"""


class RuntimeErrorMixin(RuntimeError):
    """Mixin — attach before ``Error[...]`` in MRO to make errors ``isinstance(RuntimeError)``.

    Example:
        ```python
        from forging_blocks.foundation.errors import Error, ErrorMessage


        class BrokenInvariantError(RuntimeErrorMixin, Error[str]):
            pass  # This error represents a broken invariant


        err = BrokenInvariantError(ErrorMessage("State corrupted"))
        assert isinstance(err, RuntimeError)
        ```
    """
