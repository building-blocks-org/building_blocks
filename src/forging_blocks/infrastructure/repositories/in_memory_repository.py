"""In-memory full CRUD repository backed by a dictionary.

Combines InMemoryReadRepository and InMemoryWriteRepository into a single
class suitable for non-CQRS applications or simplified contexts.
"""

from collections.abc import Mapping
from typing import Any

from forging_blocks.foundation.identified import Identified
from forging_blocks.infrastructure.repositories.in_memory_read_repository import (
    InMemoryReadRepository,
)
from forging_blocks.infrastructure.repositories.in_memory_write_repository import (
    InMemoryWriteRepository,
)


class InMemoryRepository[TEntity: Identified[Any], TId](
    InMemoryReadRepository[TEntity, TId],
    InMemoryWriteRepository[TEntity, TId],
):
    """Full CRUD in-memory repository backed by a dictionary.

    Combines read and write operations into a single class using shared
    dictionary-based storage. Suitable for non-CQRS applications or
    simplified single-process contexts.

    Example:
        ```python
        class ExpressionSpecification:
            def __init__(self, predicate):
                self._predicate = predicate

            def is_satisfied_by(self, entity):
                return self._predicate(entity)


        class MyEntity:
            def __init__(self, id: int, name: str) -> None:
                self.id = id
                self.name = name


        repo = InMemoryRepository[MyEntity, int]()
        entity = MyEntity(id=1, name="alpha")
        await repo.save(entity)
        retrieved = await repo.get_by_id(1)
        matches = await repo.find_matching(ExpressionSpecification(lambda e: e.name == "alpha"))
        await repo.delete_by_id(1)
        ```
    """

    def __init__(
        self,
        storage: Mapping[TId, TEntity] | None = None,
    ) -> None:
        """Initialize the repository with optional external storage.

        Args:
            storage: An optional mutable mapping to use as backing storage.
                If None, a new empty dictionary is used.

        """
        super().__init__()
        self._storage: dict[TId, TEntity] = dict(storage) if storage is not None else {}
