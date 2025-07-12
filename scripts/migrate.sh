#!/usr/bin/env bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <example_name>"
  exit 1
fi

EXAMPLE="$1"
EXAMPLE_DIR="examples/$EXAMPLE"
ALEMBIC_INI="$EXAMPLE_DIR/alembic.ini"

if [ ! -f "$ALEMBIC_INI" ]; then
  echo "❌ Missing alembic.ini: $ALEMBIC_INI"
  exit 1
fi

echo "🚀 Applying migrations for example: $EXAMPLE"
echo "📁 Alembic config: $ALEMBIC_INI"

cd /app

# Apply migrations using alembic upgrade
poetry run alembic -c "$ALEMBIC_INI" upgrade head

echo "✅ Migrations applied successfully."
