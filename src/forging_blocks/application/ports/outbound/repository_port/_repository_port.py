"""Full CRUD repository abstraction combining read and write interfaces."""

from ._read_only_repository_port import ReadOnlyRepositoryPort
from ._write_only_repository_port import WriteOnlyRepositoryPort


class RepositoryPort[TAggregateRoot, TId](
    ReadOnlyRepositoryPort[TAggregateRoot, TId],
    WriteOnlyRepositoryPort[TAggregateRoot, TId],
):
    """Full CRUD repository abstraction.

    Combines read and write capabilities into a single repository interface.
    Suitable for non-CQRS applications or simplified contexts.

    Example:
        ```python
        class Task:
            id: str
            name: str
            done: bool


        task = Task(id="t1", name="Review PR", done=False)
        await repo.save(task)
        found = await repo.get_by_id(task.id)
        await repo.delete_by_id(task.id)
        ```
    """
