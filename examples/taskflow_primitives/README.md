# taskflow_primitives

> Anti-pattern example demonstrating primitive obsession and anemic domain model

## 🎯 Purpose

This example demonstrates:

- **Primitive Obsession Anti-Pattern**
- **Anemic Domain Model Problems**
- **Why Value Objects Matter**
- **Scattered Business Logic Issues**
- **Comparison with Clean Implementation**

⚠️ **WARNING: This is an example of what NOT to do!**

## 🏗️ Architecture

```
src/taskflow_primitives/
├── domain/           # Pure business logic
│   ├── entities/     # Aggregates and entities
│   ├── value_objects/ # Immutable value types
│   ├── messages/     # Domain events and commands
│   └── ports/        # Domain contracts
├── application/      # Use cases and orchestration
│   ├── services/     # Use case implementations
│   ├── ports/        # Application contracts
│   └── responses/    # Output DTOs
├── infrastructure/   # External concerns
│   ├── persistence/  # Database adapters
│   ├── messaging/    # Event bus implementations
│   └── services/     # External service adapters
└── presentation/     # User interfaces
    └── cli/          # Command line interface
```

## 🚀 Getting Started

```bash
# Install dependencies
poetry install

# Run CLI
poetry run taskflow_primitives --help

# Run tests
poetry run pytest

# Quality checks (from repository root)
cd ../../
poetry run black --check examples/taskflow_primitives/
poetry run ruff check examples/taskflow_primitives/
poetry run mypy examples/taskflow_primitives/src/
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

Generated on: 2025-06-18 20:54:17 UTC
Created by: Building Blocks Example Creator v1.2.0
Author: Glauber Brennon <glauberbrennon@gmail.com>
