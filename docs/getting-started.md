# Architecture Guide

`building_blocks` embodies the best practices of **Clean Architecture** and **Hexagonal Architecture (Ports & Adapters)**, empowering you to build robust, scalable, and testable applications that are independent of frameworks, databases, or delivery channels.

---

## 🧭 Core Principles

- **Separation of Concerns:** Each layer has a clear, focused responsibility.
- **Dependency Rule:** All dependencies point inward—domain is the core and never knows about application, infrastructure, or presentation.
- **Framework Agnostic:** Core logic is independent of frameworks (FastAPI, Django, etc).
- **Port & Adapter Pattern:** Contracts (ports/interfaces) are defined in the core; implementations (adapters) live in infrastructure.

---

## 🏗️ The Layers

### 1. **Domain Layer** (Pure Core Business)

- **What:** Pure business logic—Entities, Value Objects, Aggregates, Domain Services, Domain Events.
- **How:**
  - Use `building_blocks.domain.Entity`, `AggregateRoot` for identity and event tracking.
  - No framework, DB, or technical logic here.
- **Ports:**
  - **Outbound:** Abstract base classes (interfaces) for repositories, event publishers, clocks, etc.
    - Example: `UserRepository`, `OrderEventPublisher`, `AsyncRepository`
- **Example AsyncRepository Port:**
  ```python
  class AsyncRepository(ABC, Generic[TAggregateRoot, TId]):
      """
      Generic async repository interface for aggregate roots.

      Example:
          class OrderRepository(AsyncRepository[Order, UUID]):
              async def find_by_id(self, order_id: UUID) -> Order | None: ...
              async def save(self, order: Order) -> None: ...
              async def delete(self, order: Order) -> None: ...
              async def find_all(self) -> list[Order]: ...
              async def find_by_customer_id(self, customer_id: str) -> list[Order]: ...
      """
      @abstractmethod
      async def find_by_id(self, aggregate_id: TId) -> TAggregateRoot | None: ...
      @abstractmethod
      async def save(self, aggregate: TAggregateRoot) -> None: ...
      @abstractmethod
      async def delete(self, aggregate: TAggregateRoot) -> None: ...
      @abstractmethod
      async def find_all(self) -> list[TAggregateRoot]: ...
  ```

---

### 2. **Application Layer** (Use Cases & Orchestration)

- **What:** Orchestrates business workflows and defines how external requests enter the system.
- **How:**
  - **UseCase Ports:** Abstract base classes (interfaces) for each use case.
  - **Async Support:** For IO-bound operations, use `AsyncUseCase` as your inbound port:
    ```python
    class AsyncUseCase(ABC, Generic[TRequest, TResponse]):
        """
        Application inbound port for asynchronous use cases.
        Implementations must define:
        'async def execute(self, request: TRequest) -> TResponse'
        """
        @abstractmethod
        async def execute(self, request: TRequest) -> TResponse: ...
    ```
  - **Application Services:** Concrete classes implement these ports.
  - **Request/Response:** All requests/responses are `@dataclass(frozen=True)` for immutability and clarity. This ensures that use case inputs and outputs are explicit, type-safe, and cannot be mutated.
- **Example:**
  ```python
  @dataclass(frozen=True)
  class CreateUserRequest:
      email: str
      name: str

  @dataclass(frozen=True)
  class CreateUserResponse:
      user_id: UUID

  class CreateUserUseCase(AsyncUseCase[CreateUserRequest, CreateUserResponse]):
      pass

  class CreateUserService(CreateUserUseCase):
      def __init__(self, user_repo: UserRepository):
          self.user_repo = user_repo
      async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
          ...
  ```

---

### 3. **Infrastructure Layer** (Adapters & Implementations)

- **What:** Implements all outbound ports—repositories, messaging, storage, and more.
- **Directory Structure:**
  - **Persistence Adapters:**
    - `infrastructure/persistence/models/`: ORM, ODM, or other persistence models.
      - **Models must always have `created_at` and `updated_at` fields:**
        These should be automatically managed (e.g., SQLAlchemy defaults, Pydantic, or framework support).
      - Models are responsible for mapping to/from domain objects when possible.
      - Example:
        ```python
        from datetime import datetime
        from sqlalchemy import Column, DateTime

        class UserModel(Base):
            __tablename__ = 'users'
            id = Column(UUID, primary_key=True)
            email = Column(String, nullable=False)
            name = Column(String, nullable=False)
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        ```
    - `infrastructure/persistence/repositories/`: Implements domain outbound ports with concrete classes (e.g., `SQLAlchemyUserRepository` implements `UserRepository`).
      - Mapping between persistence models and domain aggregates can be handled in repository methods or helper functions.
  - **Messaging Adapters:**
    - `infrastructure/messaging/`: Implements outbound ports for event/message brokers (e.g., Kafka, RabbitMQ).
      - Each adapter should be in its own file or subfolder for clarity.
- **Rule:**
  - Infrastructure only depends on interfaces from application/domain, never the other way around.
- **Example:**
  ```python
  # infrastructure/persistence/repositories/user_repository.py
  class SQLAlchemyUserRepository(UserRepository):
      def __init__(self, session: Session):
          self.session = session
      async def find_by_id(self, user_id: UUID) -> Optional[User]:
          # ORM logic, mapping from UserModel to User
          ...
      async def save(self, user: User) -> None:
          # ORM logic, mapping from User to UserModel
          ...
  ```

---

### 4. **Presentation Layer** (User Interfaces & Entry Points)

- **What:** REST APIs, CLI, GUIs, GRPC, etc.
- **How:**
  - Calls application layer use cases via their ports (never accessing domain or infra directly).
- **Example:**
  ```python
  @router.post("/users")
  async def create_user(req: CreateUserRequest, use_case: CreateUserUseCase = Depends()):
      return await use_case.execute(req)
  ```

---

## 🧩 Visual Overview

```
+--------------------------------------------------------------+
|                    Presentation Layer                       |
|  (Controllers, APIs, CLI, GUI, etc.)                        |
+-----------------------------+-------------------------------+
                              |
                              v
+-----------------------------+-------------------------------+
|              Application Layer (Ports & Use Cases)           |
|  +-------------------+   +-----------------------------+    |
|  |  Inbound Ports    |-->|   Application Services      |    |
|  | (UseCase/AsyncABC)|   |   (UseCase Implementations) |    |
|  +-------------------+   +-----------------------------+    |
|          |        (drives)         |                          |
|          v                         v                          |
|  +-------------------+   +-----------------------------+    |
|  |  Outbound Ports   |<--|   Adapters (Infra)          |    |
|  | (Repo/Event/Etc)  |   |   (Persistence, Messaging)  |    |
|  +-------------------+   +-----------------------------+    |
+-----------------------------+-------------------------------+
                              |
                              v
+-----------------------------+-------------------------------+
|                   Domain Layer (Pure Business)              |
|  +-------------------+   +-----------------------------+    |
|  |    Entities       |   |   Domain Services           |    |
|  |    Aggregates     |   |   Value Objects             |    |
|  |    Events         |   |   Domain Ports (ABC)        |    |
|  +-------------------+   +-----------------------------+    |
+--------------------------------------------------------------+
```

---

## 🚦 Port & Adapter Details

- **Domain Outbound Ports:**
  - *Define* in `domain/ports/` (e.g., `AsyncRepository`, `OrderEventPublisher`)
  - *Implement* in `infrastructure/persistence/repositories/` (for DB) or `infrastructure/messaging/` (for messaging)
  - **Persistence models** are in `infrastructure/persistence/models/` and must have `created_at`/`updated_at` fields auto-managed.
  - Mapping from domain to persistence can be in model methods or repository classes.

- **Application UseCase Ports:**
  - *Define* in `application/ports/` as ABCs (sync or async, e.g., `AsyncUseCase`)
  - *Implement* in `application/services/` (concrete application services)
  - **All requests and responses should be immutable dataclasses** (`@dataclass(frozen=True)`).

- **Adapters:**
  - Messaging adapters live in `infrastructure/messaging/`
  - Persistence adapters live in `infrastructure/persistence/repositories/`
  - Other infra (e.g., HTTP, file, cache) in their own subfolders.

---

## 🏆 Why This Matters

- **Testability:** Business rules can be tested without DBs or frameworks.
- **Flexibility:** Swap DBs, frameworks, or messaging platforms with zero changes to core logic.
- **Maintainability:** Modular code, clear contracts, and explicit boundaries.
- **Async First:** Native support for async use cases and repositories enables scalable, modern Python apps.

---

## 🔑 Key Takeaways

- **All dependencies point inward (toward domain).**
- **Domain is pure and unaware of frameworks/infra.**
- **Persistence adapters implement outbound ports and live in `infrastructure/persistence/repositories/`.**
- **Persistence models (with auto-managed `created_at`/`updated_at`) live in `infrastructure/persistence/models/`.**
- **Messaging adapters live in `infrastructure/messaging/`.**
- **Requests and responses for use cases are frozen dataclasses (immutable and explicit).**
- **Async ports like `AsyncUseCase` and `AsyncRepository` are first-class for modern Python.**
- **Adapters implement interfaces defined in the core.**
- **You can swap infra/frameworks with zero changes to business rules.**

---

*Build for today, evolve for tomorrow. Future-proof your business logic with Building Blocks!*
