#!/bin/bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <example_name>"
  exit 1
fi

EXAMPLE_NAME=$1
EXAMPLES_DIR="examples"
EXAMPLE_PATH="$EXAMPLES_DIR/$EXAMPLE_NAME"

# Create directories
mkdir -p "$EXAMPLE_PATH/src/domain/entities"
mkdir -p "$EXAMPLE_PATH/src/domain/ports/inbound"
mkdir -p "$EXAMPLE_PATH/src/domain/ports/outbound"
mkdir -p "$EXAMPLE_PATH/src/application/ports/inbound"
mkdir -p "$EXAMPLE_PATH/src/application/ports/outbound"
mkdir -p "$EXAMPLE_PATH/src/application/services"
mkdir -p "$EXAMPLE_PATH/src/infrastructure/persistence"
mkdir -p "$EXAMPLE_PATH/src/presentation/http"
mkdir -p "$EXAMPLE_PATH/tests"

# Create a simple Dockerfile
cat > "$EXAMPLE_PATH/Dockerfile" <<EOF
FROM python:3.9-slim
WORKDIR /app
COPY ../../pyproject.toml ../../poetry.lock /app/
RUN pip install poetry && poetry install --no-root
COPY . /app
CMD ["poetry", "run", "uvicorn", "src.presentation.http.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

echo "Created example structure and Dockerfile for '$EXAMPLE_NAME'"

# Update central docker-compose.yml

COMPOSE_FILE="docker-compose.yml"

# Compose service entry snippet
SERVICE_ENTRY="
  $EXAMPLE_NAME:
    build:
      context: ./examples/$EXAMPLE_NAME
    container_name: ${EXAMPLE_NAME}_container
    ports:
      - \"8000\"
    environment:
      - ENVIRONMENT=development
    depends_on: []
"

# Check if service already exists
if grep -q "^\s*$EXAMPLE_NAME:" "$COMPOSE_FILE"; then
  echo "Service '$EXAMPLE_NAME' already exists in $COMPOSE_FILE, skipping add."
else
  echo "Adding service '$EXAMPLE_NAME' to $COMPOSE_FILE"
  # Insert before "volumes:" or at end if no volumes section
  if grep -q "volumes:" "$COMPOSE_FILE"; then
    # Insert before volumes:
    sed -i "/volumes:/i$SERVICE_ENTRY" "$COMPOSE_FILE"
  else
    # Append at end
    echo "$SERVICE_ENTRY" >> "$COMPOSE_FILE"
  fi
fi

echo "Done."
