from collections.abc import Mapping

from forging_blocks.foundation.errors.error import Error


class UnitOfWorkError[MetadataType: Mapping[str, object] = dict[str, object]](Error[MetadataType]):
    """Error raised when a Unit of Work operation fails."""

    pass
