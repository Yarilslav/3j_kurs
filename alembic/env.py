from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.engine import make_url

from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from app.core.config import settings
from app.db.base import Base
import app.models  # noqa: F401


target_metadata = Base.metadata

def run_migrations_offline() -> None:

    url = make_url(settings.DATABASE_URL)
    if url.drivername.endswith("+psycopg_async"):
        url = url.set(drivername="postgresql+psycopg")
    url = str(url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    url = make_url(settings.DATABASE_URL)
    if url.drivername.endswith("+psycopg_async"):
        url = url.set(drivername="postgresql+psycopg")
    connectable = create_engine(
        str(url),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
