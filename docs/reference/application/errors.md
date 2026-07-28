# Application Errors

Application-level errors represent failures that occur during use case execution.
They are distinct from domain errors (which describe rule violations in the problem
space) and foundation errors (which describe general-purpose failures like invalid
arguments). Application errors signal infrastructure or coordination problems:
a transaction that won't commit, an event store that can't append, a concurrency
conflict between competing updates.

- **UnitOfWorkError** — Transaction commit or rollback failure
- **EventStoreError** — Event append or retrieval failure
- **ConcurrencyError** — Optimistic concurrency conflict
- **EventBusError** — Event publishing failure

## When to use

Raise these errors from application code when a use case fails due to infrastructure or coordination issues. They extend the [Foundation](../foundation.md) `Error` base class, so they carry structured messages and work with the presentation error pipeline.

!!! note "On error boundaries"
    Application errors describe *what failed* during coordination. They should not encode transport or presentation concerns — those belong to outer layers.
