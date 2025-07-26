## Running Migration Scripts

To generate a migration for an example:

1. Ensure your containers are running:
   ```bash
   docker compose up --build
   ```

2. Run generate migration inside the container:
   ```bash
   docker compose exec <example_name> ./scripts/generate_migration.sh <example_name> "<migration_message>"
   ```
   - `<example_name>`: The name of your example (matches directory under `examples/`).
   - `<migration_message>`: A short message describing your migration.

3. After generating the migration, run the migration script:
```bash
docker compose exec <example_name> ./scripts/migrate.sh <example_name>
```

### Example Usage
To generate and run a migration for the `tasker_primitive_obsession` example, your commands would look like this:
```bash
docker compose exec tasker_primitive_obsession ./scripts/generate_migration.sh tasker_primitive_obsession "Create Task table"
docker compose exec tasker_primitive_obsession ./scripts/migrate.sh tasker_primitive_obsession
```

### Important Notes
- Ensure you are running these commands from the root of the project directory.
- The `generate_migration.sh` script creates a new migration file.
- The `migrate.sh` script applies the migration to the database.
- These scripts are designed to be run inside the Docker container for the specific example you are working on.

> **Note:** Running this script from your host is not recommended.
