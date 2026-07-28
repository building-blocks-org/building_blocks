from dataclasses import dataclass, field


@dataclass(frozen=True)
class ErrorMetadata[T]:
    """Represents metadata about the error."""

    context: dict[str, T] = field(default_factory=lambda: {})
