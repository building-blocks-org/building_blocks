"""Mixin that makes forging-blocks errors catchable as built-in RuntimeError."""


class RuntimeErrorMixin(RuntimeError):
    """Mixin — attach before ``Error[...]`` in MRO to make errors ``isinstance(RuntimeError)``."""
