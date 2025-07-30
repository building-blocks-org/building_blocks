#!/usr/bin/env bash
set -e

# Usage: ./scripts/run_example.sh [example_name]
# Defaults to "tasker_primitive_obsession" if no argument is given or EXAMPLE env var is not set.

EXAMPLE=${1:-${EXAMPLE:-tasker_primitive_obsession}}

# Check that the migration script exists
if [[ ! -x ./scripts/migrate.sh ]]; then
  echo "Error: ./scripts/migrate.sh not found or not executable."
  exit 1
fi

# Run migrations for the current example
./scripts/migrate.sh "$EXAMPLE"

# Check that the main app module exists (python import path check)
MAIN_MODULE="examples.$EXAMPLE.src.presentation.http.main"
PYTHON_MAIN_PATH="examples/$EXAMPLE/src/presentation/http/main.py"
if [[ ! -f "$PYTHON_MAIN_PATH" ]]; then
  echo "Error: Main module $PYTHON_MAIN_PATH not found."
  exit 1
fi

echo "Starting the HTTP server for $EXAMPLE..."
exec poetry run uvicorn "$MAIN_MODULE:app" --host 0.0.0.0 --port 8000 --reload
