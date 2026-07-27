"""Error raised when a transaction operation fails."""
from collections.abc import Mapping


from forging_blocks.foundation.errors.error import Error


class TransactionError[MetadataType: Mapping[str, object] = dict[str, object]](Error[MetadataType]):
    """Error raised when a transaction operation fails."""

    pass
