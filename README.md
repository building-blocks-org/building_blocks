# Building Blocks 🏗️

A clean architecture Python library following hexagonal principles for building robust, maintainable applications.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-dependency%20management-blue.svg)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Why Building Blocks?

**The Problem** 🤔
Most Python applications start simple but become maintenance nightmares:

Business logic mixed with web framework code
Hard to test without running the entire application
Switching databases or frameworks requires rewriting everything
Domain expertise gets buried in technical implementation details

The Solution ✨
Building Blocks separates what your app does from how it does it:

✅ Test your business logic without databases or web servers
✅ Switch frameworks without changing your core business code
✅ Maintain clean boundaries between layers
✅ Scale your team with clear architectural patterns

Who Should Use This? 👥

Teams building long-term maintainable applications
Developers who want to learn clean architecture patterns
Projects that need framework flexibility
Applications with complex business logic

## Overview

Building Blocks provides a foundation for implementing clean architecture patterns in Python applications. It offers framework-agnostic components that help you build maintainable, testable, and scalable software following Domain-Driven Design (DDD) and hexagonal architecture principles.

## Features

- 🎯 **Framework Agnostic**: Works with any Python web framework or application type
- 🏛️ **Clean Architecture**: Implements hexagonal architecture patterns
- 🧩 **Domain-Driven Design**: Provides building blocks for DDD implementation
- 🔒 **Type Safe**: Full type annotations with mypy support
- 🧪 **Well Tested**: Comprehensive test coverage
- 📚 **Well Documented**: Clear documentation and examples
- ⚡ **Modern Python**: Built for Python 3.9+ with modern syntax

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                     │
│                 (Primary Adapters)                      │
│                                                         │
│              Any Framework or Interface                 │
│        (Web, CLI, Desktop, Mobile, etc.)               │
└─────────────────────┬───────────────────────────────────┘
                      │ (depends on)
                      ▼
      ┌─────────────────────────────────────────────────────┐
      │            Application Layer                        │
      │                                                     │
      │  ┌─────────────────────────────────────────────┐    │
      │  │        Application Inbound Ports            │    │
      │  │     (Use Cases, Command/Query Handlers)     │    │
      │  │        (Interfaces/Abstract Classes)        │    │
      │  └─────────────────┬───────────────────────────┘    │
      │                    ▲ (implements)                   │
      │                    │                                │
      │  ┌─────────────────┴───────────────────────────┐    │
      │  │        Application Services                 │    │
      │  │   (Implementations of Inbound Ports)        │    │
      │  │         (Concrete Classes)                  │    │
      │  └─────────────────┬───────────────────────────┘    │
      │                    │ (depends on)                   │
      │                    ▼                                │
      │  ┌─────────────────────────────────────────────┐    │
      │  │       Application Outbound Ports            │    │
      │  │    (External Services, Notifications)       │    │
      │  │        (Interfaces/Abstract Classes)        │    │
      │  └─────────────────────────────────────────────┘    │
      └─────────────┬───────────────────────────────────────┘
                    │ (depends on)
                    ▼
┌─────────────────────────────────────────────────────────┐
│                   Domain Layer                          │
│                  (Business Logic)                       │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Entities   │  │  Value      │  │   Aggregates    │  │
│  │             │  │  Objects    │  │                 │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │          Domain Inbound Ports                   │    │
│  │        (Domain Service Interfaces)              │    │
│  │        (Interfaces/Abstract Classes)            │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    ▲ (implements)                       │
│                    │                                    │
│  ┌─────────────────┴───────────────────────────────┐    │
│  │           Domain Services                       │    │
│  │     (Implementations of Inbound Ports)          │    │
│  │           (Concrete Classes)                    │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │ (depends on)                       │
│                    ▼                                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │         Domain Outbound Ports                   │    │
│  │    (Repository, Event Publisher, Clock)         │    │
│  │        (Interfaces/Abstract Classes)            │    │
│  │           **DEFINED BY DOMAIN**                 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                      ▲ (implements)
                      │
┌─────────────────────┴───────────────────────────────────┐
│                  Infrastructure Layer                   │
│                 (Secondary Adapters)                    │
│                                                         │
│         Implementations of all Outbound Ports          │
│      (Database, External APIs, Message Queues)         │
│               (Concrete Classes)                        │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Principles ✅

1. **Dependencies Point Inward**: All arrows point toward the domain layer
2. **Domain is Independent**: Domain layer has ZERO outward dependencies
3. **Dependency Inversion**: Infrastructure implements domain-defined interfaces
4. **Interfaces in Domain**: Outbound ports are contracts defined by the domain
5. **Clean Boundaries**: Each layer only knows about the layer inside it

## Port Architecture

Building Blocks follows proper hexagonal architecture with clear port separation between Domain and Application layers:

> **Important Note**: All **Ports** are contracts defined as **interfaces** (using `ABC` and `@abstractmethod`) or **abstract classes**. All **Services** and **Infrastructure** components are **concrete implementations** of these contracts.

### Domain Layer Ports

**Domain Inbound Ports** (Entry points to Domain):
- **Domain Service Interfaces**: Abstract base classes defining domain service contracts
- Implemented by Domain Services in the same layer

**Domain Services** (Implementations of Domain Inbound Ports):
- **Domain Service Implementations**: Concrete classes implementing complex business logic

**Domain Outbound Ports** (Infrastructure contracts defined by Domain):
- **Repository Interfaces**: Abstract base classes for data persistence contracts
- **Domain Event Publisher Interfaces**: Abstract classes for publishing domain events
- **Clock Interfaces**: Abstract classes for time-related operations
- **ID Generation Interfaces**: Abstract classes for unique identifier generation

### Application Layer Ports

**Application Inbound Ports** (Use case entry points):
- **Use Case Interfaces**: Abstract base classes defining application workflows
- **Command Handler Interfaces**: Abstract classes for commands that modify state
- **Query Handler Interfaces**: Abstract classes for queries that read state
- **Application Event Handler Interfaces**: Abstract classes for application-level events

**Application Services** (Implementations of Application Inbound Ports):
- **Use Case Implementations**: Concrete classes that orchestrate domain objects
- **Command Handler Implementations**: Concrete classes that process commands
- **Query Handler Implementations**: Concrete classes that execute queries
- **Application Event Handler Implementations**: Concrete classes for cross-cutting concerns

**Application Outbound Ports** (Application service contracts):
- **Integration Event Publisher Interfaces**: Abstract classes for cross-service communication
- **Message Bus Interfaces**: Abstract classes for command and event routing
- **External API Service Interfaces**: Abstract classes for third-party integrations
- **Notification Service Interfaces**: Abstract classes for email, SMS, push notifications
- **File Storage Service Interfaces**: Abstract classes for file operations
- **Caching Service Interfaces**: Abstract classes for application-level caching

### Code Examples: Interfaces vs Implementations

```python
# Domain Outbound Port (Interface) - DEFINED BY DOMAIN
class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None: ...

    @abstractmethod
    async def find_by_id(self, user_id: str) -> User | None: ...

# Application Inbound Port (Interface)
class CreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, command: CreateUserCommand) -> User: ...

# Application Service (Implementation) - DEPENDS ON DOMAIN INTERFACES
class CreateUserUseCaseImpl(CreateUserUseCase):  # Concrete implementation
    def __init__(self, user_repository: UserRepository):  # Depends on DOMAIN interface
        self._user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> User:
        # Concrete implementation logic
        pass

# Infrastructure (Implementation) - IMPLEMENTS DOMAIN INTERFACES
class SQLAlchemyUserRepository(UserRepository):  # Implements DOMAIN interface
    def __init__(self, session: Session):
        self._session = session

    async def save(self, user: User) -> None:
        # Concrete database implementation
        pass
```

### Key Distinction: Events

```python
# Domain Layer - Domain Event Publisher (Interface DEFINED BY DOMAIN)
class DomainEventPublisher(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None: ...

# Application Layer - Integration Event Publisher (Interface)
class IntegrationEventPublisher(ABC):
    @abstractmethod
    async def publish_user_welcomed(self, user_id: str, email: str) -> None: ...

class MessageBus(ABC):
    @abstractmethod
    async def send_command(self, command: Command, target_service: str) -> None: ...
```

## Installation

### Requirements

- Python 3.9+
- Poetry (recommended) or pip

### Using Poetry (Recommended)

```bash
poetry add building-blocks
```

### Using pip

```bash
pip install building-blocks
```

## Quick Start

### 1. Define a Domain Entity

```python
from building_blocks.domain.entities import BaseEntity

class User(BaseEntity[str]):
    def __init__(self, user_id: str, email: str, name: str):
        super().__init__(user_id)
        self.email = email
        self.name = name

    def change_email(self, new_email: str) -> None:
        # Domain logic here
        if not new_email or '@' not in new_email:
            raise ValueError("Invalid email address")
        self.email = new_email
```

### 2. Create Value Objects

```python
from building_blocks.domain.value_objects import ValueObject

class Email(ValueObject):
    def __init__(self, value: str):
        if not value or '@' not in value:
            raise ValueError("Invalid email address")
        self.value = value

class Money(ValueObject):
    def __init__(self, amount: int, currency: str):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.amount = amount
        self.currency = currency
```

### 3. Define Domain Outbound Ports (Repository Interfaces)

```python
from abc import ABC, abstractmethod
from building_blocks.domain.ports.outbound import Repository

class UserRepository(Repository[User, str]):  # Abstract base class
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass
```

### 4. Define Application Inbound Ports (Use Case Interfaces)

```python
from abc import ABC, abstractmethod
from building_blocks.application.ports.inbound import UseCase

class CreateUserUseCase(UseCase[CreateUserCommand, User]):  # Abstract base class
    @abstractmethod
    async def execute(self, command: CreateUserCommand) -> User:
        pass
```

### 5. Implement Application Services (Use Case Implementations)

```python
from building_blocks.application.services import CreateUserUseCaseImpl

class CreateUserUseCaseImpl(CreateUserUseCase):  # Concrete implementation
    def __init__(
        self,
        user_repository: UserRepository,  # Interface dependency
        email_service: EmailNotificationService  # Interface dependency
    ):
        self._user_repository = user_repository
        self._email_service = email_service

    async def execute(self, command: CreateUserCommand) -> User:
        # Concrete implementation logic
        existing_user = await self._user_repository.find_by_email(command.email)
        if existing_user:
            raise ValueError("User already exists")

        user = User(
            user_id=generate_id(),
            email=command.email,
            name=command.name
        )

        await self._user_repository.save(user)
        await self._email_service.send_welcome_email(user.email, user.name)

        return user
```

### 6. Use in Your Presentation Layer

The presentation layer can be any framework or interface. Check our examples:

- [FastAPI Example](examples/fastapi/) - REST API with dependency injection
- [CLI Example](examples/cli/) - Command-line interface
- [Flask Example](examples/flask/) - Web application

## Core Components

### Presentation Layer (Primary Adapters)

- **Web APIs**: Any web framework (FastAPI, Flask, Django, etc.)
- **CLI Applications**: Any CLI framework (Click, Typer, argparse, etc.)
- **Desktop Applications**: Any GUI framework (Tkinter, Qt, etc.)
- **Mobile Applications**: Any mobile framework
- **Message Consumers**: Event/message handlers

### Application Layer

#### Application Inbound Ports (Driving Side) - **Interfaces/Abstract Classes**
- **Use Case Interfaces**: Application-specific business rules and workflows
- **Command Handler Interfaces**: Handle commands that modify state
- **Query Handler Interfaces**: Handle queries that read state
- **Application Event Handler Interfaces**: Handle application and integration events

#### Application Services (Implementations) - **Concrete Classes**
- **Use Case Implementations**: Orchestrate domain objects and services
- **Command Handler Implementations**: Process commands and coordinate workflows
- **Query Handler Implementations**: Execute queries and return data
- **Application Event Handler Implementations**: Handle cross-cutting concerns

#### Application Outbound Ports (Driven Side) - **Interfaces/Abstract Classes**
- **Integration Event Publisher Interfaces**: Cross-service communication contracts
- **External Service Interfaces**: Third-party service contracts
- **Notification Interfaces**: Communication contracts
- **Message Bus Interfaces**: Command/event routing contracts

### Domain Layer (Core)

- **Entities**: Objects with identity that encapsulate business logic
- **Value Objects**: Immutable objects that represent descriptive aspects
- **Aggregates**: Clusters of domain objects treated as a single unit
- **Domain Events**: Events that represent domain occurrences

#### Domain Inbound Ports (Entry Points) - **Interfaces/Abstract Classes**
- **Domain Service Interfaces**: When domain services need external access

#### Domain Services (Implementations) - **Concrete Classes**
- **Domain Service Implementations**: Complex business logic that doesn't belong to a single entity

#### Domain Outbound Ports (Infrastructure Contracts) - **Interfaces/Abstract Classes**
- **Repository Interfaces**: Data persistence contracts defined by domain
- **Domain Event Publisher Interfaces**: Publish domain events within bounded context
- **Clock Interfaces**: Time-related contracts
- **ID Generator Interfaces**: Unique identifier generation contracts

### Infrastructure Layer (Secondary Adapters) - **Concrete Classes**

- **Repository Implementations**: Concrete implementations of domain repository interfaces
- **External Service Adapters**: Integrate with external systems
- **Database Implementations**: Any database technology
- **Messaging Systems**: Any event bus or message queue technology

## Project Structure

```
src/building_blocks/
├── domain/
│   ├── entities/                # Concrete classes
│   ├── value_objects/           # Concrete classes
│   ├── aggregates/              # Concrete classes
│   ├── events/                  # Concrete classes
│   ├── services/                # Concrete implementations of Domain Inbound Ports
│   └── ports/
│       ├── inbound/            # Abstract base classes (interfaces)
│       └── outbound/           # Abstract base classes (interfaces)
├── application/
│   ├── services/               # Concrete implementations of Application Inbound Ports
│   └── ports/
│       ├── inbound/           # Abstract base classes (interfaces)
│       └── outbound/          # Abstract base classes (interfaces)
├── infrastructure/
│   ├── adapters/              # Concrete implementations of all outbound ports
│   ├── repositories/          # Concrete implementations of domain repositories
│   └── external/              # Concrete implementations of application services
└── presentation/
    └── common/                # Framework-agnostic presentation utilities
```

## Examples

Check out the `/examples` directory for complete working examples with different frameworks:

- [**FastAPI Example**](examples/fastapi/) - REST API with dependency injection and OpenAPI
- [**Flask Example**](examples/flask/) - Web application with templates
- [**CLI Example**](examples/cli/) - Command-line interface with Click
- [**Django Example**](examples/django/) - Full web application (Coming Soon)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/gbrennon/building-blocks.git
cd building-blocks

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install

# Run tests
poetry run pytest

# Run type checking
poetry run mypy src

# Run linting
poetry run black src tests
poetry run isort src tests
poetry run bandit -r src
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/domain/test_entities.py

# Run with verbose output
poetry run pytest -v
```

### Code Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **MyPy**: Static type checking
- **Bandit**: Security linting
- **Pre-commit**: Git hooks for code quality
- **Pytest**: Testing framework

```bash
# Run all quality checks
poetry run pre-commit run --all-files
```

## Documentation

- 📖 [**Full Documentation**](https://building-blocks.readthedocs.io/) (Coming Soon)
- 🎯 [**Architecture Guide**](docs/architecture.md)
- 🚀 [**Getting Started**](docs/getting-started.md)
- 📚 [**API Reference**](docs/api-reference.md)
- 💡 [**Examples**](examples/)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks (`poetry run pre-commit run --all-files`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] **v0.1.0**: Domain building blocks (Current)
- [ ] **v0.2.0**: Application layer with Application Inbound and Outbound Ports
- [ ] **v0.3.0**: Infrastructure abstractions and adapters
- [ ] **v0.4.0**: Presentation layer helpers for multiple frameworks
- [ ] **v0.5.0**: Event sourcing support
- [ ] **v0.6.0**: CQRS implementation
- [ ] **v1.0.0**: Stable API with full documentation

## Support

- 📧 **Email**: [glauberbrennon@gmail.com](mailto:glauberbrennon@gmail.com)
- 🐛 **Issues**: [GitHub Issues](https://github.com/gbrennon/building-blocks/issues)
- 🐛 **Issues**: [GitHub Issues](https://github.com/gbrennon/building-blocks/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/gbrennon/building-blocks/discussions)

## Inspiration

This library is inspired by:

- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) by Alistair Cockburn
- [Domain-Driven Design](https://www.domainlanguage.com/ddd/) by Eric Evans
- [Implementing Domain-Driven Design](https://www.informit.com/store/implementing-domain-driven-design-9780321834577) by Vaughn Vernon

---

**Built with ❤️ by [Glauber Brennon](https://github.com/gbrennon)**
