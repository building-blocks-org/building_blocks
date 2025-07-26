## Running Migration Scripts

To generate a migration for an example project:

1. Ensure your containers are running:
   ```bash
   docker compose up --build
   ```

2. Run a migration generation inside the container:
   ```bash
   docker compose exec <example_name> ./scripts/generate_migration.sh <example_name> "<migration_message>"
   ```
   - `<example_name>`: The name of your example (matches directory under `examples/`).
   - `<migration_message>`: A short message describing your migration.

Example:
```bash
docker compose exec tasker_primitives ./scripts/generate_migration.sh tasker_primitives "Add new feature"

docker compose exec tasker_primitives ./scripts/migrate.sh tasker_primitives
```

> **Note:** Running this script from your host is not recommended.
