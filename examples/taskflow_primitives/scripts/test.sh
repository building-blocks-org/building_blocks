#!/bin/bash
# Test script for project
# Run from project directory

set -e

PROJECT_NAME=$(basename "$(pwd)")
echo "🧪 Running tests for $PROJECT_NAME..."

poetry run pytest tests/ -v --cov="src/$PROJECT_NAME" --cov-report=term-missing

echo "✅ All tests passed!"
