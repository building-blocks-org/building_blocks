# taskflow

> Clean Architecture with DDD Example showcasing building-blocks library

## 🎯 Purpose

This example demonstrates:

- **Clean Architecture** (Hexagonal Architecture)
- **Domain-Driven Design (DDD)**
- **SOLID Principles**
- **Event-Driven Architecture**
- **CQRS Pattern**
- **Building Blocks Library Usage**

## 🏗️ Architecture

```
src/taskflow/
├── domain/           # Pure business logic
│   ├── entities/     # Aggregates and entities
│   ├── value_objects/ # Immutable value types
│   ├── messages/     # Domain events and commands
│   ├── services/     # Domain services
│   └── ports/        # Domain contracts
├── application/      # Use cases and orchestration
│   ├── services/     # Use case implementations
│   ├── ports/        # Application contracts
│   ├── requests/     # Input DTOs
│   ├── handlers/     # Event and command handlers
│   └── responses/    # Output DTOs
├── infrastructure/   # External concerns
│   ├── persistence/  # Database adapters
│   ├── messaging/    # Event bus implementations
│   └── services/     # External service adapters
└── presentation/     # User interfaces
    ├── api/          # REST API
    └── cli/          # Command line interface
```

## 🚀 Getting Started

```bash
# Install dependencies
poetry install

# Run CLI
poetry run taskflow --help

# Run API server
poetry run uvicorn taskflow.presentation.api.main:app --reload

# Run tests
poetry run pytest

# Quality checks (from repository root)
cd ../../
poetry run black --check examples/taskflow/
poetry run ruff check examples/taskflow/
poetry run mypy examples/taskflow/src/
```

## 📚 Learning Path

1. **Domain Layer** - Start with entities and value objects
2. **Application Layer** - Understand use cases and ports
3. **Infrastructure** - See how external concerns are handled
4. **Presentation** - Learn about clean interfaces

## 🔗 Related

- Main library: `../../src/building_blocks/`
- Other examples: `../`

## 📖 Documentation

Generated on: 2025-06-18 15:46:57 UTC
Created by: Building Blocks Example Creator v1.2.0
Author: Glauber Brennon <glauberbrennon@gmail.com>
