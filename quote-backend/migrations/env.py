import os
from logging.config import fileConfig

from flask import current_app
from alembic import context
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Alembic Config object
config = context.config

# Apply database URL from .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Setup logging
fileConfig(config.config_file_name)

# Get metadata from Flask SQLAlchemy db instance
target_metadata = current_app.extensions['migrate'].db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = current_app.extensions['migrate'].db.engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
