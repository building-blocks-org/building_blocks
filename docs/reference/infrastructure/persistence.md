# Persistence

Persistence bridges domain aggregates and storage. Forging Blocks ships in-memory
implementations so applications can run without external databases — useful for tests,
development, and single-process deployments. The in-memory store uses identity-keyed
dictionaries; swap in a real database adapter behind the same `RepositoryPort` for production.

## Repositories

- **InMemory Repository** — Shared identity-keyed storage: `get_by_id`, `save`, `delete_by_id`
- **In-Memory Write Repository** — Dictionary-backed append-only store for testing
- **In-Memory Read Repository** — Query-oriented read store for CQRS projections
- **Aggregate Repository** — Integrates with `UnitOfWorkPort` and `EventBusPort`;
  tracks new and dirty aggregates, publishes collected events on commit

## Unit of Work

Manages a transactional boundary around repository operations. Tracks new and dirty
aggregates, flushes events on commit, provides `commit`/`rollback` semantics.
Multiple repository operations within a single use case are treated as one atomic unit.

## When to use

Use the in-memory implementations for tests and development — no external dependencies.
`InMemoryRepository` gives you `get_by_id`/`save`/`delete_by_id`; extend it for domain-specific
queries. Use `AggregateRepository` when you need `UnitOfWorkPort` integration and event
publishing.
