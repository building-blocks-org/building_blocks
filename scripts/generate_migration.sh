#!/usr/bin/env bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <example_name> [migration_message]"
  exit 1
fi

EXAMPLE="$1"
MESSAGE="${2:-auto_migration}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REV_ID="${TIMESTAMP}"

EXAMPLE_DIR="examples/$EXAMPLE"
ALEMBIC_INI="$EXAMPLE_DIR/alembic.ini"
VERSIONS_DIR="$EXAMPLE_DIR/src/infrastructure/persistence/migrations/versions"

# Verify paths are correct inside container
if [ ! -f "$ALEMBIC_INI" ]; then
  echo "❌ Missing alembic.ini: $ALEMBIC_INI"
  exit 1
fi

if [ ! -d "$VERSIONS_DIR" ]; then
  echo "❌ Missing versions directory: $VERSIONS_DIR"
  exit 1
fi

echo "🚀 Generating migration for example: $EXAMPLE"
echo "📁 Alembic config: $ALEMBIC_INI"
echo "📁 Versions directory: $VERSIONS_DIR"

# Run from project root
cd /app

# Execute alembic using the dev dependencies we installed
poetry run alembic -c "$ALEMBIC_INI" revision \
  --autogenerate \
  --message "$MESSAGE" \
  --rev-id "$REV_ID" \
  --version-path "$VERSIONS_DIR"

echo "✅ Migration created in: $VERSIONS_DIR"
