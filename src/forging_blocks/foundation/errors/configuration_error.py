"""Configuration error for invalid runtime settings.

Defines ``ConfigurationError``, raised when a component is configured
with settings that fall outside the allowed range or format (e.g.,
disallowed URL schemes, invalid filesystem paths, or out-of-range
parameters).
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.value_error_mixin import ValueErrorMixin
from forging_blocks.foundation.errors.core import ErrorMessage, MetadataValueType


class ConfigurationError(ValueErrorMixin, Error[MetadataValueType]):
    """Raised when a component receives invalid configuration.

    This error signals operational misconfiguration at runtime —
    for example, a URL with a disallowed scheme, an invalid
    filesystem path, or an out-of-range parameter value.
    """

    def __init__(self, message: str) -> None:
        """Initialise with a descriptive configuration-violation message.

        Args:
            message: Human-readable description of the misconfiguration,
                including the offending value and the acceptable range.

        """
        super().__init__(ErrorMessage(message))
