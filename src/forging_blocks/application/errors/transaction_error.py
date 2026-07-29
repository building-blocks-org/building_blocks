"""Error raised when a transaction operation fails."""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin


class TransactionError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Error raised when a transaction operation fails."""
