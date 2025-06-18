#!/bin/bash
# Development setup for project

set -e

PROJECT_NAME=$(basename "$(pwd)")
echo "🔧 Setting up development environment for $PROJECT_NAME..."

# Install dependencies
echo "Installing dependencies..."
poetry install

# Verify setup
echo "Verifying setup..."
poetry run python -c "from building_blocks.domain import Entity; print('✅ Dependencies verified')"

# Run initial tests
echo "Running initial tests..."
poetry run pytest tests/ -v

echo "✅ Development environment ready!"
echo ""
echo "Next steps:"
echo "  1. Implement domain layer"
echo "  2. Add application services"
echo "  3. Create infrastructure adapters"
echo "  4. Build presentation layer"
