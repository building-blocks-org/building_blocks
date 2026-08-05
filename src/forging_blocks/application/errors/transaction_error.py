"""Application-layer transaction boundary error.

Defines ``TransactionError``, raised when a transaction boundary operation
in the application layer fails — covering failures during transaction
begin, commit, or rollback.

Extends ``RuntimeErrorMixin`` so it is catchable as ``RuntimeError``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin


class TransactionError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Raised when a transaction boundary operation fails.

    Covers failures during transaction begin, commit, or rollback.
    Extends ``RuntimeErrorMixin`` so it is catchable as
    ``RuntimeError``.

    Example:
        ```python
        error = TransactionError.from_string("Transaction commit failed")
        ```

    """
