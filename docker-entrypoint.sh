#!/usr/bin/env bash
set -e

EXAMPLE=${EXAMPLE:-tasker_primitive_obsession}

./scripts/migrate.sh "$EXAMPLE"

echo "Starting the HTTP server for $EXAMPLE..."
exec poetry run uvicorn "examples.$EXAMPLE.src.presentation.http.main:app" --host 0.0.0.0 --port 8000 --reload
