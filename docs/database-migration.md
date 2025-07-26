## Running Migration Scripts

To generate a migration for an example project:

1. Ensure your containers are running:
   ```bash
   docker compose up --build
   ```

2. Run a migration generation inside the container:
   ```bash
   docker compose exec <example_name> ./scripts/generate_migration.sh <example_name> <migration_name>

3. Apply the migration:
   ```bash
   docker compose exec <example_name> ./scripts/apply_migration.sh <example_name>
   ```

> **Note:** Running those scripts from your host is not recommended because it may lead to issues such as:
> - Dependency mismatches: The script relies on specific tools and libraries that are installed in the container but may not be available or compatible on your host system.
> - Environment inconsistencies: The container provides a controlled environment that ensures the script runs as intended, whereas the host environment may introduce unexpected variables.
> - Potential failures: Missing configurations or tools on the host system can cause the script to fail.
>
> To avoid these issues, always run the script inside the container as described above.
