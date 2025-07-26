from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parents[5] / ".env")
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from examples.tasker_primitive_obsession.src.infrastructure.config import (
    get_app_settings,
)
from examples.tasker_primitive_obsession.src.infrastructure.persistence.models.base import (
    Base,
)

# -----------------------------------------
# Alembic Config
# -----------------------------------------
config = context.config
app_settings = get_app_settings()

target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override the sqlalchemy.url in alembic config with the sync driver URL
sync_database_url = app_settings.database_url.replace("asyncpg", "psycopg2")
config.set_main_option("sqlalchemy.url", sync_database_url)


# -----------------------------------------
# Offline Migrations
# -----------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------------------------
# Online Migrations
# -----------------------------------------
def run_migrations_online() -> None:
    """Run migrations synchronously in 'online' mode."""
    connectable = create_engine(
        sync_database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------------------
# Entry point
# -----------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
