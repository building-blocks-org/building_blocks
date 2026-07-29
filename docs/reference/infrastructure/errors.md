# Infrastructure Errors

Infrastructure errors represent failures in the technical implementation
layer — persistence, transport, and external integration.

## Concrete error types

- **RepositoryError** — Base for all repository operation failures
- **RepositoryNotFoundError** — Deletion or retrieval of an aggregate that does not exist

All infrastructure errors use `RuntimeErrorMixin`, making them catchable as
`RuntimeError`.

## When to use

Subclass `RepositoryError` for concrete repository-level failures. Raise them
from infrastructure adapter code when persistence or retrieval operations fail.
They extend the [Foundation](../foundation.md) `Error` base class, so they carry
structured messages and integrate with the presentation error pipeline.

!!! note "On error boundaries"
    Infrastructure errors describe *what failed* at the technical layer. They
    should not encode domain rules or presentation concerns — those belong to
    their respective layers.
