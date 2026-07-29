from forging_blocks.foundation.errors.base.error import Error


class UnitOfWorkError[MetadataValueType = object](Error[MetadataValueType]):
    """Error raised when a Unit of Work operation fails."""
