from typing import Self

from forging_blocks.domain.messages.message import MessageMetadata
from forging_blocks.domain.messages.query import Query


class SimpleFakeQuery(Query[dict[str, object]]):
    """Minimal fake query used to exercise dispatch paths."""

    def __init__(self, name: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._name = name

    @property
    def _payload(self) -> dict[str, object]:
        return {"name": self._name}

    @property
    def value(self) -> dict[str, object]:
        return self._payload

    @classmethod
    def from_payload_fields(cls, data: dict[str, object], metadata: MessageMetadata) -> Self:
        return cls(name=str(data.get("name", "")), metadata=metadata)
