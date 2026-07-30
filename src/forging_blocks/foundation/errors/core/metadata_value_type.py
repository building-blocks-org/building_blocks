"""Type alias for metadata values used in Error and ErrorMetadata.

This alias is intentionally permissive to allow any value in metadata
while still enabling type-safe usage in generic Error classes.
"""

from typing import TypeAlias

MetadataValueType: TypeAlias = object
