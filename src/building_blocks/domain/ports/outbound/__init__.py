"""
Outbound ports module.
Contains interfaces for external dependencies, implemented by infrastructure layer.
"""

from building_blocks.domain.ports.outbound.convenience_repository import (
    UUIDReadOnlyRepository,
    UUIDRepository,
    UUIDWriteOnlyRepository,
)
from building_blocks.domain.ports.outbound.read_only_repository import (
    ReadOnlyRepository,
)
from building_blocks.domain.ports.outbound.repository import Repository
from building_blocks.domain.ports.outbound.unit_of_work import UnitOfWork
from building_blocks.domain.ports.outbound.write_only_repository import (
    WriteOnlyRepository,
)

__all__ = [
    "Repository",
    "ReadOnlyRepository",
    "WriteOnlyRepository",
    "UnitOfWork",
    # Convenience classes for UUID-based aggregates
    "UUIDRepository",
    "UUIDReadOnlyRepository",
    "UUIDWriteOnlyRepository",
]
