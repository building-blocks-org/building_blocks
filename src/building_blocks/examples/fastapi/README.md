# Building Blocks 🏗️

A clean architecture Python library following hexagonal principles for building robust, maintainable applications.

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-dependency%20management-blue.svg)](https://python-poetry.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Overview

Building Blocks provides a foundation for implementing clean architecture patterns in Python applications. It offers framework-agnostic components that help you build maintainable, testable, and scalable software following Domain-Driven Design (DDD) and hexagonal architecture principles.

## Features

- 🎯 **Framework Agnostic**: Works with any Python web framework or application type
- 🏛️ **Clean Architecture**: Implements hexagonal architecture patterns
- 🧩 **Domain-Driven Design**: Provides building blocks for DDD implementation
- 🔒 **Type Safe**: Full type annotations with mypy support
- 🧪 **Well Tested**: Comprehensive test coverage
- 📚 **Well Documented**: Clear documentation and examples
- ⚡ **Modern Python**: Built for Python 3.13+ with modern syntax

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                     │
│                    (Adapters)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Web API   │  │     CLI     │  │      GUI        │  │
│  │  (FastAPI,  │  │   (Click,   │  │   (Tkinter,     │  │
│  │   Flask)    │  │   Typer)    │  │    Qt, etc.)    │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────┬───────────────┬───────────────┬───────────┘
              │               │               │
              ▼               ▼               ▼
      ┌─────────────────────────────────────────────────────┐
      │            Application Layer                        │
      │                                                     │
      │  ┌─────────────────────────────────────────────┐    │
      │  │            Ports/Inbound                    │    │
      │  │  ┌─────────────┐  ┌─────────────────────┐   │    │
      │  │  │   Use Cases │  │   Command/Query     │   │    │
      │  │  │             │  │     Handlers        │   │    │
      │  │  └─────────────┘  └─────────────────────┘   │    │
      │  └─────────────────────────────────────────────┘    │
      │                                                     │
      │  ┌─────────────────────────────────────────────┐    │
      │  │           Ports/Outbound                    │    │
      │  │  ┌─────────────┐  ┌─────────────────────┐   │    │
      │  │  │ Repository  │  │   External Service  │   │    │
      │  │  │ Interfaces  │  │    Interfaces       │   │    │
      │  │  └─────────────┘  └─────────────────────┘   │    │
      │  └─────────────────────────────────────────────┘    │
      └─────────────┬───────────────────────────┬───────────┘
                    │                           │
                    ▼                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Domain Layer                          │
│                   (Core Logic)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Entities   │  │  Value      │  │   Domain        │  │
│  │             │  │  Objects    │  │   Services      │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │ Aggregates  │  │   Domain    │  │    Events       │  │
│  │             │  │    Rules    │  │                 │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────┬───────────────┬───────────────┬───────────┘
              │               │               │
              ▼               ▼               ▼
┌─────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                   │
│                     (Adapters)                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │  Database   │  │ External    │  │   Messaging     │  │
│  │ (SQLAlchemy,│  │   APIs      │  │   (Redis,       │  │
│  │  MongoDB)   │  │ (REST, gRPC)│  │   RabbitMQ)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Installation

### Requirements

- Python 3.13+
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

### 3. Define Outbound Ports (Repository Interfaces)

```python
from abc import ABC, abstractmethod
from building_blocks.application.ports.outbound import Repository

class UserRepository(Repository[User, str]):
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        pass
```

### 4. Implement Inbound Ports (Use Cases)

```python
from building_blocks.application.ports.inbound import UseCase

class CreateUserUseCase(UseCase[CreateUserCommand, User]):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> User:
        # Check if user already exists
        existing_user = await self._user_repository.find_by_email(command.email)
        if existing_user:
            raise ValueError("User already exists")

        # Create new user
        user = User(
            user_id=generate_id(),
            email=command.email,
            name=command.name
        )

        # Save user
        await self._user_repository.save(user)
        return user
```

### 5. Create Presentation Layer (FastAPI Example)

```python
from fastapi import FastAPI, HTTPException, Depends
from building_blocks.presentation.fastapi import Router

app = FastAPI(title="Building Blocks Example")

@app.post("/users", response_model=UserResponse)
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    try:
        command = CreateUserCommand(
            email=request.email,
            name=request.name
        )
        user = await use_case.execute(command)
        return UserResponse.from_entity(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Core Components

### Presentation Layer (Primary Adapters)

- **Web APIs**: REST APIs using FastAPI, Flask, Django
- **CLI Applications**: Command-line interfaces using Click, Typer
- **Desktop GUIs**: Desktop applications using Tkinter, Qt
- **Web UIs**: Server-side rendered UIs with templates

### Application Layer (Ports)

#### Inbound Ports (Driving Side)
- **Use Cases**: Application-specific business rules and workflows
- **Command Handlers**: Handle commands that modify state
- **Query Handlers**: Handle queries that read state
- **Event Handlers**: Handle domain and integration events

#### Outbound Ports (Driven Side)
- **Repository Interfaces**: Data persistence contracts
- **External Service Interfaces**: Third-party service contracts
- **Event Publisher Interfaces**: Event publishing contracts
- **Notification Interfaces**: Communication contracts

### Domain Layer (Core)

- **Entities**: Objects with identity that encapsulate business logic
- **Value Objects**: Immutable objects that represent descriptive aspects
- **Aggregates**: Clusters of domain objects treated as a single unit
- **Domain Services**: Stateless services that contain domain logic
- **Domain Events**: Events that represent domain occurrences
- **Domain Rules**: Business rules and invariants

### Infrastructure Layer (Secondary Adapters)

- **Repository Implementations**: Concrete implementations of repository interfaces
- **External Service Adapters**: Integrate with external systems
- **Database Implementations**: ORM/ODM integrations (SQLAlchemy, MongoDB)
- **Messaging Systems**: Event bus, message queues (Redis, RabbitMQ)

## Project Structure

```
src/building_blocks/
├── domain/
│   ├── entities/
│   ├── value_objects/
│   ├── aggregates/
│   ├── services/
│   └── events/
├── application/
│   ├── ports/
│   │   ├── inbound/     # Use Cases, Command/Query Handlers
│   │   └── outbound/    # Repository & Service Interfaces
│   └── services/
├── infrastructure/
│   ├── adapters/
│   ├── repositories/
│   └── external/
└── presentation/
    ├── web/
    ├── cli/
    └── gui/
```

## Examples

Check out the `/examples` directory for complete working examples:

- [**E-commerce API**](examples/ecommerce/) - FastAPI with order management and aggregates
- [**User Management CLI**](examples/user_management_cli/) - Click-based CLI application
- [**Banking System**](examples/banking/) - Money transfers with domain events
- [**Task Management Web**](examples/task_management/) - Flask web application

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

- [ ] **v0.1.0**: Core domain building blocks (Current)
- [ ] **v0.2.0**: Application layer with ports/inbound and ports/outbound
- [ ] **v0.3.0**: Infrastructure abstractions and adapters
- [ ] **v0.4.0**: Presentation layer helpers (FastAPI, Flask, CLI)
- [ ] **v0.5.0**: Event sourcing support
- [ ] **v0.6.0**: CQRS implementation
- [ ] **v1.0.0**: Stable API with full documentation

## Support

- 📧 **Email**: [glauberbrennon@gmail.com](mailto:glauberbrennon@gmail.com)
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
