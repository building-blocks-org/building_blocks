# Building Blocks - Development Automation
# Author: Glauber Brennon <glauberbrennon@gmail.com>

.PHONY: help create-project examples docs quality test clean

# Default target
help: ## Show this help message
	@echo "🚀 Building Blocks Development Commands"
	@echo "======================================"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "📚 Quick Start:"
	@echo "  make create-project name=taskflow"
	@echo "  make examples"
	@echo "  make help-interactive"

help-interactive: ## Launch interactive help system
	@./scripts/help.sh

create-project: ## Create new example project (usage: make create-project name=PROJECT_NAME type=PROJECT_TYPE)
	@if [ -z "$(name)" ]; then \
		echo "❌ Error: Project name required"; \
		echo "Usage: make create-project name=PROJECT_NAME [type=PROJECT_TYPE]"; \
		echo "Example: make create-project name=taskflow type=clean-ddd"; \
		exit 1; \
	fi
	@./scripts/create-example-project.sh $(name) $(if $(type),--type $(type))

examples: ## Show example project creation commands
	@echo "📋 Example Project Creation Commands"
	@echo "=================================="
	@echo ""
	@echo "Basic Examples:"
	@echo "  make create-project name=taskflow"
	@echo "  make create-project name=user_service type=microservice"
	@echo "  make create-project name=bad_example type=primitive-obsession"
	@echo ""
	@echo "Learning Path:"
	@echo "  make create-project name=learning_clean type=clean-ddd"
	@echo "  make create-project name=learning_bad type=primitive-obsession"
	@echo "  make create-project name=learning_events type=event-driven"

docs: ## Build and serve documentation
	@echo "📚 Building documentation..."
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs serve; \
	else \
		echo "📖 Local documentation available at:"; \
		find docs -name "*.md" | head -10; \
		echo "..."; \
		echo ""; \
		echo "💡 Install mkdocs for better experience: pip install mkdocs"; \
	fi

quality: ## Run all quality checks
	@echo "🔍 Running quality checks..."
	@poetry run black --check src/ examples/
	@poetry run ruff check src/ examples/
	@poetry run mypy src/
	@poetry run bandit -r src/
	@echo "✅ Quality checks passed!"

test: ## Run all tests (library + examples)
	@echo "🧪 Running tests..."
	@poetry run pytest tests/ -v
	@for example in examples/*/; do \
		if [ -f "$$example/pyproject.toml" ]; then \
			echo "Testing $$(basename "$$example")..."; \
			cd "$$example" && poetry run pytest tests/ -v && cd - >/dev/null; \
		fi; \
	done
	@echo "✅ All tests passed!"

clean: ## Clean up generated files and caches
	@echo "🧹 Cleaning up..."
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -delete
	@find . -type d -name ".mypy_cache" -delete
	@find . -type f -name "*.pyc" -delete
	@rm -rf .coverage htmlcov/
	@echo "✅ Cleanup complete!"

install: ## Install development dependencies
	@echo "📦 Installing dependencies..."
	@poetry install
	@echo "✅ Dependencies installed!"

format: ## Format code with black and ruff
	@echo "🎨 Formatting code..."
	@poetry run black src/ examples/ tests/
	@poetry run ruff check --fix src/ examples/ tests/
	@echo "✅ Code formatted!"

check: quality test ## Run quality checks and tests

setup-dev: install ## Complete development environment setup
	@echo "🔧 Setting up development environment..."
	@poetry install
	@if command -v pre-commit >/dev/null 2>&1; then \
		pre-commit install; \
		echo "✅ Pre-commit hooks installed"; \
	fi
	@echo "✅ Development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  make create-project name=my_first_example"
	@echo "  make help-interactive"

release: ## Create a new release (maintainers only)
	@echo "🚀 Creating release..."
	@./scripts/release.sh

project-types: ## List all available project types
	@./scripts/create-example-project.sh --list-types

wizard: ## Launch project creation wizard
	@./scripts/help.sh
