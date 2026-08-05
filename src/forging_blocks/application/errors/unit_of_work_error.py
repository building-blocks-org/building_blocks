"""Base error for Unit of Work transaction failures.

Defines ``UnitOfWorkError``, raised when a commit or rollback operation
fails in the application layer's transactional boundary. Extends
``RuntimeErrorMixin`` so it is catchable as ``RuntimeError``.
"""

from forging_blocks.foundation.errors.base.error import Error
from forging_blocks.foundation.errors.builtin.runtime_error_mixin import RuntimeErrorMixin


class UnitOfWorkError[MetadataValueType = object](RuntimeErrorMixin, Error[MetadataValueType]):
    """Raised when a Unit of Work commit or rollback fails.

    Indicates failure within the application layer's transactional
    boundary. Extends ``RuntimeErrorMixin`` so it is catchable as
    ``RuntimeError``.

    Example:
        ```python
        error = UnitOfWorkError.from_string("Unit of Work rollback failed")
        ```

    """
