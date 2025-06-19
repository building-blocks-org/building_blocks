#!/bin/bash
# Quality check for project
# Run from project directory

set -e

PROJECT_NAME=$(basename "$(pwd)")
echo "🔍 Running quality checks for $PROJECT_NAME..."

# Run from repository root to use shared configuration
cd ../../

echo "  → Black formatting check..."
poetry run black --check "examples/$PROJECT_NAME/src/" "examples/$PROJECT_NAME/tests/"

echo "  → Ruff linting..."
poetry run ruff check "examples/$PROJECT_NAME/src/" "examples/$PROJECT_NAME/tests/"

echo "  → MyPy type checking..."
poetry run mypy "examples/$PROJECT_NAME/src/"

echo "  → Bandit security check..."
poetry run bandit -r "examples/$PROJECT_NAME/src/"

echo "✅ All quality checks passed!"
