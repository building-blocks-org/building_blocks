# Building Blocks - Quick Reference

## 🚀 Essential Commands

```bash
# Create new project
./scripts/create-example-project.sh PROJECT_NAME [--type TYPE]

# Or use make
make create-project name=PROJECT_NAME type=TYPE

# Interactive help
make help-interactive
./scripts/help.sh
```

## 📋 Project Types

| Type | Purpose | Best For |
|------|---------|----------|
| `clean-ddd` | Full clean architecture | Learning, reference |
| `primitive-obsession` | Anti-pattern example | Training, comparison |
| `event-driven` | CQRS + Event Sourcing | Distributed systems |
| `microservice` | API-focused service | Service architecture |
| `monolith` | Modular monolith | Large system design |

## 🔧 Common Workflows

```bash
# Learning path
make create-project name=learning_clean type=clean-ddd
make create-project name=learning_bad type=primitive-obsession

# Development workflow
cd examples/my_project
poetry shell
./scripts/dev-setup.sh
poetry run pytest

# Quality checks
make quality
make test
```

## 📚 Documentation

- `make help` - Show all commands
- `make help-interactive` - Interactive help
- `docs/tooling/` - Detailed documentation
- `examples/*/README.md` - Project-specific docs

## 🆘 Quick Help

```bash
./scripts/create-example-project.sh --help      # Tool help
./scripts/create-example-project.sh --examples  # Usage examples
./scripts/create-example-project.sh --list-types # Project types
```
