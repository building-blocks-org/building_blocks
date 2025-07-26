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
# After generating the migration, run the following command to apply it:
docker compose exec tasker_primitives ./scripts/migrate.sh tasker_primitives
```

> **Note:** Running this script from your host is not recommended because it may lead to issues such as:
> - Dependency mismatches: The script relies on specific tools and libraries that are installed in the container but may not be available or compatible on your host system.
> - Environment inconsistencies: The container provides a controlled environment that ensures the script runs as intended, whereas the host environment may introduce unexpected variables.
> - Potential failures: Missing configurations or tools on the host system can cause the script to fail.
> 
> To avoid these issues, always run the script inside the container as described above.
