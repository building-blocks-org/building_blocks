# Infrastructure Layer 🏗️

The **infrastructure layer** provides the technical implementations that enable your application and domain layers to interact with the outside world.
It contains concrete adapters for outbound ports (interfaces) declared in the domain and application layers.

---

## 📁 Directory Structure

```
infrastructure/
├── crypto/         # Cryptography and security adapters (e.g., hashing, encryption)
├── messaging/      # Messaging systems (e.g., message queues, event buses)
└── persistence/    # Persistence adapters (e.g., database, file storage)
```

---

## ✨ Core Concepts

- **Adapters:**
  Infrastructure implements generic outbound ports—such as repositories and notifiers—defined in the domain and application layers.
  This enables you to swap out technical details (e.g., change databases, messaging providers) without touching your core business logic.

- **No Business Logic:**
  Infrastructure should never contain business rules. It is purely technical.

- **Examples:**
  - A SQLAlchemy repository implements an `AsyncRepository[Order, UUID]` interface from the domain.
  - An SMTP email sender implements the `Notifier` interface from the application layer.
  - A Redis-based event publisher implements an `EventPublisher` port.

---

## 🧩 How to Use

1. **Implement Generic Outbound Ports**
   - For each outbound port (interface) defined in your domain or application layer (such as `AsyncRepository` or `Notifier`), provide a concrete implementation in this layer.

   ```python
   # Example: SQLAlchemy repository for a domain aggregate
   from building_blocks.domain.ports.outbound.repository import AsyncRepository
   from typing import Any
   from uuid import UUID

   # Suppose you have a domain aggregate root:
   class Order:
       def __init__(self, order_id: UUID, customer_id: str) -> None:
           self.order_id = order_id
           self.customer_id = customer_id

   class SQLAlchemyOrderRepository(AsyncRepository[Order, UUID]):
       async def find_by_id(self, order_id: UUID) -> Order | None:
           # Implementation using SQLAlchemy to find the order
           ...

       async def save(self, order: Order) -> None:
           # Implementation using SQLAlchemy to save the order
           ...

       async def delete(self, order: Order) -> None:
           # Implementation using SQLAlchemy to delete the order
           ...

       async def find_all(self) -> list[Order]:
           # Implementation using SQLAlchemy to fetch all orders
           ...
   ```

2. **Organize by Technology or Concern**
   - Place adapters in the relevant subdirectory:
     - `crypto/` for cryptography, hashing, etc.
     - `messaging/` for message bus, event publishing, queues.
     - `persistence/` for database, file storage, or other I/O (e.g., repositories).

3. **Keep Dependencies Outward**
   - Infrastructure can depend on any external library or system.
   - It should never depend on your application's or domain's business logic, only on the outbound port interfaces.

---

## 🏗️ Why This Matters

- **Swappability:** Easily replace or extend technical solutions with minimal changes.
- **Isolation:** Keeps all technical complexity out of your core application and domain.
- **Testability:** Allows you to mock or stub infrastructure in your tests.
- **Type Safety:** By implementing generic interfaces (e.g., `AsyncRepository[Aggregate, IdType]`), you gain flexibility and type safety for all adapters.

---

## 🧑‍💻 Extending the Infrastructure Layer

- Add new adapters as your technical needs grow (e.g., new databases, message brokers, cryptography providers).
- Implement each outbound port interface (such as `AsyncRepository` or `Notifier`) defined by your domain or application layer here.
- Use type parameters to ensure that each adapter is explicit, type-safe, and flexible.

---

**For more examples and usage, see the project root [README](../../README.md) and the `/examples` directory.**
