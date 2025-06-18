# Architecture Guide

`building_blocks` is designed around the principles of Clean Architecture and Hexagonal Architecture (Ports and Adapters). This guide provides a deep dive into the structure and philosophy of the library.

## Core Principles

- **Separation of Concerns**: Strict separation between domain, application, and infrastructure layers.
- **Dependency Rule**: Dependencies flow inwards. The domain layer has no knowledge of application/infrastructure/presentation.
- **Framework Agnostic**: Core logic is independent of frameworks (FastAPI, Django, etc).

## Layers

### 1. Domain Layer
The heart of your application: business logic, entities, rules.
Contains Entities, Value Objects, Aggregates, Domain Services, Domain Events.

- Use: `building_blocks.domain.Entity`, `AggregateRoot` for identity/events.
- Pure Python; no framework or DB logic here!

### 2. Application Layer
Orchestrates use cases and defines application boundaries ("ports").

- Contains: Application Services (Use Cases), Inbound/Outbound Ports (abstract base classes).
- Use: `building_blocks.application.UseCase`, `Port` for clean boundaries.

### 3. Infrastructure Layer (Adapters)
Implements outbound ports, connects to DB, frameworks, external services.

- Contains: Repositories, message brokers, framework adapters, etc.
- Only depends on interfaces from the application/domain.

### 4. Presentation Layer
User-facing entry points: web, CLI, desktop, etc.
Only depends on application layer, never on domain or infra directly.

---

## ASCII Diagram

```
+----------------------------------------------------------------+
|                        Presentation Layer                      |
|        (Controllers, Views, CLI Commands, etc.)                |
+----------------------------------------------------------------+
                                |
                                v
+------------------------------+-------------------------------+
|             Application Layer (Ports & Use Cases)             |
|  +-------------------+   +-----------------------+           |
|  |  Inbound Ports    |-->|  Application Services |           |
|  |  (Use Case ABCs)  |   |   (Orchestration)     |           |
|  +-------------------+   +-----------------------+           |
|          |         (drives)        |                          |
|          v                         v                          |
|  +-------------------+   +-----------------------+           |
|  |  Outbound Ports   |<--|  Adapters/Repos       |           |
|  |  (Repo/Infra ABCs)|   |  (Infra Implementations)          |
|  +-------------------+   +-----------------------+           |
+------------------------------+-------------------------------+
                                |
                                v
+------------------------------+-------------------------------+
|                     Domain Layer                             |
|  +-------------------+   +-----------------------+           |
|  |    Entities       |   |   Domain Services     |           |
|  +-------------------+   +-----------------------+           |
+--------------------------------------------------------------+
```

---

## Port Architecture

- **Inbound Ports**: Abstract base classes for use cases (application API). Called by presentation layer.
- **Outbound Ports**: Interfaces for infrastructure needs (repos, notifications, etc). Implemented by adapters.

This enforces testable, maintainable, framework-agnostic business logic.

---

## Key Takeaways

- **All dependencies point inward (toward domain).**
- **Domain is pure and unaware of frameworks/infra.**
- **Adapters implement interfaces defined inside (not outside).**
- **You can swap infra/frameworks with zero changes to business rules.**

---
