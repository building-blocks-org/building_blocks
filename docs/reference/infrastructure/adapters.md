# Technical Adapters

Technical adapters implement the outbound ports defined by the Application layer — they
are the "other side" of the port/adapter boundary. Forging Blocks ships technology-agnostic
implementations that depend only on the Python standard library, so applications can use
them at runtime without pulling in third-party dependencies.

The adapters below all satisfy their corresponding port contracts. In tests, use them
directly; in production, swap in real implementations (database, HTTP client, filesystem)
behind the same port interface.

## Logging
A standard-library logging adapter implementing `LoggerPort`. Provides `debug`, `info`, `warning`, and `error` methods — all accept `*args: str` for ``%``-style formatting (delegates to `logging.Logger`).

## HTTP Client
A `urllib`-based HTTP client implementing `HttpClientPort`. Supports GET, POST, headers, and timeout configuration.

## File System
An OS-level filesystem adapter implementing `FileSystemPort`. All operations are `async`. Supports `read`, `write`, `delete`, `exists`, and directory listing.

## Caching
A dictionary-backed key-value cache implementing `CachePort`. Supports `get`, `set`, `delete`, and `clear`.

## Serialization

`MessageCodec` is an abstract codec base that defines `encode` / `decode` for bidirectional message serialization. `DictMessageCodec` is the concrete ``dict[str, object]`` implementation that ships with Forging Blocks.

These adapters implement the corresponding outbound ports from Application. Use the in-memory versions for tests; swap to real implementations (database, HTTP, filesystem) in production.
