from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin


class UnitOfWorkError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Error raised when a Unit of Work operation fails."""
