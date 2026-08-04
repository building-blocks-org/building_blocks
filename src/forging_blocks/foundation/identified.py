"""Protocol for domain objects that carry an identifier."""

from typing import Protocol


class Identified[IdentityType](Protocol):
    """Protocol for objects that expose an ``id`` property.

    Satisfied by any object whose ``id`` returns the object's identity,
    which may be ``None`` for draft/unpersisted instances.

    Example:
        ```python
        class User(Identified[int]):
            def __init__(self, user_id: int, name: str) -> None:
                self._id = user_id
                self.name = name

            @property
            def id(self) -> int | None:
                return self._id


        user = User(42, "Alice")
        assert user.id == 42
        ```
    """

    @property
    def id(self) -> IdentityType | None: ...
