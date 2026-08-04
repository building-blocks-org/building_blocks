# Messaging and Events

The messaging layer routes commands, queries, and events between application
and domain components. Three building blocks compose to form the full pipeline:

- **Message Bus** — dispatches any message to the right handler (commands, queries, events).
  `MessageBusCommandSender`, `MessageBusEventPublisher`, and `MessageBusQueryFetcher` are thin port-satisfying wrappers
  around the bus that expose narrower, role-specific interfaces.
- **Event Store** — an append-only log that records domain events chronologically.
  Enables rebuilding aggregate state from history (event sourcing).
- **Event Bus** — publish/subscribe delivery of domain events to registered handlers.
  Sits behind `EventPublisherPort` so subscribers can be composed and replaced.

## Message Bus

- **In-Memory Message Bus** — Synchronous dispatcher routing commands, queries, and events to registered handlers.
- **Command Sender** — Thin adapter implementing `CommandSenderPort`; fire-and-forget.
- **Event Publisher** — Thin adapter implementing `EventPublisherPort`; publishes domain events.
- **Query Fetcher** — Thin adapter implementing `QueryFetcherPort`; dispatches queries, returns typed results.

## Event Store

Append-only event log storing domain events chronologically. Supports `append` with optimistic concurrency (expected version check) and `get_events` for aggregate rebuilding.

## Event Bus

Publish/subscribe mechanism delivering domain events to registered handlers. Synchronous delivery to all subscribers.

## When to use

Use the in-memory message bus for tests and development. Register handlers at startup, dispatch messages at runtime. Use `MessageBusCommandSender`, `MessageBusEventPublisher`, and `MessageBusQueryFetcher` as thin wrappers that satisfy the corresponding port protocols.
