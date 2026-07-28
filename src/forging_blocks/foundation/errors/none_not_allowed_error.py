"""Error indicating that a None value was provided where it is not allowed."""

from forging_blocks.foundation.errors.base.error import Error


class NoneNotAllowedError(Error[str]):
    """Error indicating that a None value was provided where it is not allowed."""
