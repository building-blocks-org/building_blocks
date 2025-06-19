# Building Blocks Tooling Documentation

Welcome to the Building Blocks tooling ecosystem! This directory contains documentation for all development tools, scripts, and utilities that make working with the building-blocks library efficient and enjoyable.

## 📚 Quick Navigation

| Document | Purpose | Audience |
|----------|---------|----------|
| [Project Creator](project-creator.md) | Create example projects | Developers, Teams |
| [Development Workflow](development-workflow.md) | Day-to-day development | Contributors |
| [Quality Gates](quality-gates.md) | Code quality standards | All developers |
| [Release Process](release-process.md) | Library releases | Maintainers |
| [Troubleshooting](troubleshooting.md) | Common issues | Everyone |

## 🚀 Quick Start

```bash
# Create your first example project
./scripts/create-example-project.sh my_first_project

# See all available options
./scripts/create-example-project.sh --help

# Get comprehensive examples
./scripts/create-example-project.sh --examples
```

## 🎯 Common Scenarios

### New Developer Onboarding
```bash
# 1. Create learning project
./scripts/create-example-project.sh learning_ddd --type clean-ddd

# 2. Create anti-pattern comparison
./scripts/create-example-project.sh learning_ddd_bad --type primitive-obsession

# 3. Start development
cd examples/learning_ddd && poetry shell
```

### Architecture Training Workshop
```bash
# Create workshop materials
./scripts/create-example-project.sh workshop_clean --type clean-ddd
./scripts/create-example-project.sh workshop_events --type event-driven
./scripts/create-example-project.sh workshop_antipatterns --type primitive-obsession
```

### Production Project Bootstrap
```bash
# Create microservice template
./scripts/create-example-project.sh user_service --type microservice

# Customize for your needs
cd examples/user_service
# ... implement your domain logic
```

## 🔧 Available Tools

| Tool | Location | Purpose |
|------|----------|---------|
| `create-example-project.sh` | `scripts/` | Create new example projects |
| `quality-check.sh` | `scripts/` | Run all quality checks |
| `test-all.sh` | `scripts/` | Test library + all examples |
| `release.sh` | `scripts/` | Automated releases |

## 📖 Further Reading

- [Contributing Guidelines](../CONTRIBUTING.md)
- [Architecture Decision Records](../adr/)
- [API Documentation](../api/)
- [Examples Gallery](../examples/)
