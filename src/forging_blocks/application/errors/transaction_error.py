"""Error raised when a transaction operation fails."""

from forging_blocks.foundation.errors.base.error import Error


class TransactionError[MetadataValueType = object](Error[MetadataValueType]):
    """Error raised when a transaction operation fails."""

    pass
