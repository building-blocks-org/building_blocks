#!/usr/bin/env bash
set -e

./scripts/migrate.sh tasker_primitives

echo "Starting the HTTP server..."
exec poetry run uvicorn examples.tasker_primitives.src.presentation.http.main:app --host 0.0.0.0 --port 8000 --reload
