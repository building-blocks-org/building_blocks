# Project Creator Tool

The `create-example-project.sh` script is your gateway to exploring building-blocks library capabilities through hands-on examples.

## 🎯 Overview

This tool creates fully-structured, production-ready example projects that demonstrate different architectural patterns and complexity levels using the building-blocks library.

## 📋 Quick Reference Card

```bash
# Basic usage
./scripts/create-example-project.sh <name>

# Common options
--type <type>      # Project type (clean-ddd, primitive-obsession, etc.)
--force           # Overwrite existing project
--dry-run         # Preview without creating
--verbose         # Detailed output
--examples        # Show usage examples
--list-types      # List all project types
```

## 🏗️ Project Types Deep Dive

### clean-ddd (Default)
**Perfect for: Learning, reference implementations, onboarding**

```bash
./scripts/create-example-project.sh taskflow
```

**What you get:**
- ✅ Complete domain layer with rich entities and value objects
- ✅ Application services implementing use cases
- ✅ Infrastructure adapters for persistence and messaging
- ✅ CLI interface with Typer and Rich
- ✅ FastAPI REST endpoints
- ✅ Comprehensive test suite with 90%+ coverage
- ✅ Event-driven architecture with domain events
- ✅ CQRS separation for commands and queries

**File structure:**
```
src/taskflow/
├── domain/
│   ├── entities/task.py           # Rich aggregate roots
│   ├── value_objects/             # Immutable types
│   ├── messages/events/           # Domain events
│   ├── services/                  # Domain services
│   └── ports/                     # Contracts
├── application/
│   ├── services/                  # Use case implementations
│   ├── requests/responses/        # DTOs
│   └── handlers/                  # Event handlers
├── infrastructure/
│   ├── persistence/               # Repository implementations
│   ├── messaging/                 # Event bus adapters
│   └── services/                  # External service adapters
└── presentation/
    ├── cli/main.py               # Typer CLI app
    └── api/main.py               # FastAPI application
```

### primitive-obsession
**Perfect for: Training, code reviews, refactoring workshops**

```bash
./scripts/create-example-project.sh taskflow_bad --type primitive-obsession
```

**What you get:**
- ❌ Anemic domain models (just data containers)
- ❌ Primitive types everywhere (strings, ints, bools)
- ❌ Business logic scattered across service layers
- ❌ No type safety or compile-time validation
- ❌ Tight coupling and violation of DDD principles
- ❌ Hard-to-test, hard-to-maintain code

**Educational value:**
- Shows exactly what NOT to do
- Demonstrates pain points of traditional approaches
- Perfect for before/after comparisons
- Highlights the value of domain modeling

### event-driven
**Perfect for: Distributed systems, microservices architecture**

```bash
./scripts/create-example-project.sh event_store --type event-driven
```

**What you get:**
- ✅ Event sourcing patterns
- ✅ CQRS with separate read/write models
- ✅ Event handlers and projections
- ✅ Saga pattern for complex workflows
- ✅ Async processing with proper error handling
- ✅ Event versioning and migration strategies

### microservice
**Perfect for: API development, service boundaries**

```bash
./scripts/create-example-project.sh user_api --type microservice
```

**What you get:**
- ✅ FastAPI with OpenAPI documentation
- ✅ Health checks and monitoring endpoints
- ✅ Circuit breaker patterns
- ✅ API versioning strategies
- ✅ Container-ready configuration
- ✅ Service boundary enforcement

### monolith
**Perfect for: Legacy modernization, large system design**

```bash
./scripts/create-example-project.sh ecommerce --type monolith
```

**What you get:**
- ✅ Multiple bounded contexts
- ✅ Shared kernel patterns
- ✅ Module communication strategies
- ✅ Evolution path to microservices
- ✅ Domain event integration across contexts

## 🎨 Customization Patterns

### Development Workflow Integration

```bash
# Create project with immediate development setup
./scripts/create-example-project.sh my_project && \
cd examples/my_project && \
poetry shell && \
./scripts/dev-setup.sh
```

### Team Collaboration

```bash
# Create consistent training environment
for dev in alice bob charlie; do
    ./scripts/create-example-project.sh "training_${dev}" --type clean-ddd
done
```

### Architecture Comparison Studies

```bash
# Create comparison set
./scripts/create-example-project.sh orders_clean --type clean-ddd
./scripts/create-example-project.sh orders_events --type event-driven
./scripts/create-example-project.sh orders_bad --type primitive-obsession

# Now compare approaches side-by-side
```

## 🔧 Advanced Usage

### Environment Variables

```bash
# Customize default settings
export BB_PROJECT_AUTHOR="Your Name"
export BB_PROJECT_EMAIL="your.email@company.com"
export BB_DEFAULT_PROJECT_TYPE="microservice"

./scripts/create-example-project.sh my_service
```

### Automation and CI/CD

```bash
# Automated testing of project creation
./scripts/create-example-project.sh test_project --dry-run
if [ $? -eq 0 ]; then
    ./scripts/create-example-project.sh test_project --force
    cd examples/test_project && poetry run pytest
fi
```

### Batch Operations

```bash
# Create multiple projects for workshop
project_types=("clean-ddd" "primitive-obsession" "event-driven")
for type in "${project_types[@]}"; do
    ./scripts/create-example-project.sh "workshop_${type//-/_}" --type "$type"
done
```

## 🐛 Troubleshooting

### Common Issues

**"Project already exists"**
```bash
# Solution: Use --force or choose different name
./scripts/create-example-project.sh existing_name --force
```

**"Poetry not found"**
```bash
# Solution: Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

**"Building-blocks import failed"**
```bash
# Solution: Ensure you're in the right directory
cd /path/to/building-blocks
./scripts/create-example-project.sh project_name
```

### Debug Mode

```bash
# Get detailed information about what's happening
./scripts/create-example-project.sh debug_project --verbose --dry-run
```

### Validation

```bash
# Verify project was created correctly
cd examples/your_project
poetry run pytest tests/test_setup.py -v
```

## 📊 Success Metrics

After creating a project, you should be able to:

1. ✅ Import building-blocks components
2. ✅ Run all tests successfully
3. ✅ Execute quality checks without errors
4. ✅ Start implementing domain logic immediately
5. ✅ Use the CLI/API interfaces

```bash
# Verify success
cd examples/your_project
poetry run python -c "from building_blocks.domain import Entity; print('✅ Success!')"
poetry run pytest tests/ -v
./scripts/quality-check.sh
```

## 🔗 Related Documentation

- [Development Workflow](development-workflow.md)
- [Quality Gates](quality-gates.md)
- [Architecture Patterns](../architecture/)
- [Examples Gallery](../examples/)

## 💡 Pro Tips

1. **Start with clean-ddd** - It's the most comprehensive example
2. **Create comparison projects** - Build both clean and anti-pattern versions
3. **Use --dry-run first** - Preview before creating large projects
4. **Leverage automation** - Script common project creation patterns
5. **Document customizations** - Keep notes on project-specific changes

---

*Last updated: 2025-01-18 05:09:14 UTC*
*Author: Glauber Brennon <glauberbrennon@gmail.com>*
