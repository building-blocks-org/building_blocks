# Project Structure

This project follows a hexagonal architecture pattern with clear separation of concerns.

## Domain Layer Structure

```
domain/
├── entities/           # Domain entities and value objects
├── ports/
│   ├── inbound/       # Interfaces for use cases (implemented by domain services)
│   └── outbound/      # Interfaces for external dependencies (implemented by infrastructure)
└── services/          # Domain services implementing inbound ports
```

## Testing Guidelines

- **Test Class Naming**: `Test<TestedClass>`
- **Test Method Naming**: `test_<tested_method>_when_<scenario>_then_<result>`
- **Test Structure**: Follow AAA (Arrange, Act, Assert) pattern
- **Interaction Rule**: Only one interaction with the tested method per test (in Act section)
- **Unit Tests**: Mocking allowed and encouraged
- **Integration Tests**: Avoid mocks when possible, but allowed if necessary

## Getting Started

1. Start by defining your core domain entities
2. Identify the key use cases and define inbound ports
3. Identify external dependencies and define outbound ports
4. Implement domain services
5. Write comprehensive tests following the guidelines
