"""Mixin that makes forging-blocks errors catchable as built-in ValueError."""


class ValueErrorMixin(ValueError):
    """Mixin — attach before ``Error[...]`` in MRO to make errors ``isinstance(ValueError)``."""
