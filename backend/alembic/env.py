from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel
import sys
import os

# Add the backend/src directory to the Python path so we can import our models
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# Import all models to register them with SQLModel metadata
from models.task import Task  # noqa: F401
from models.user import User  # noqa: F401

# Phase III: Import chatbot models directly (avoid importing services to prevent circular imports)
# The chatbot.models module only contains SQLModel definitions
import importlib.util
chatbot_models_path = os.path.join(os.path.dirname(__file__), "..", "src", "chatbot", "models.py")
spec = importlib.util.spec_from_file_location("chatbot_models", chatbot_models_path)
chatbot_models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(chatbot_models)
Conversation = chatbot_models.Conversation  # noqa: F401
Message = chatbot_models.Message  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target_metadata to SQLModel's metadata
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # Get the database URL from environment settings
    try:
        from core.config import get_settings
        settings = get_settings()
        url = settings.database_url
    except Exception:
        # Fallback to a dummy URL if settings can't be loaded
        url = "postgresql://user:pass@localhost/db"

    context.configure(
        url=url,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
        # Don't use connection for offline mode
    )

    # For autogenerate in offline mode, we need to use a special approach
    # Check if this is a revision command with autogenerate
    context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the database URL from environment settings
    try:
        from core.config import get_settings
        settings = get_settings()

        # Override the sqlalchemy.url with our database URL
        config.set_main_option("sqlalchemy.url", settings.database_url)
    except Exception:
        # Fallback to a dummy URL if settings can't be loaded
        config.set_main_option("sqlalchemy.url", "postgresql://user:pass@localhost/db")

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Check if this is a revision command by looking at sys.argv
import sys
if 'revision' in sys.argv or '--autogenerate' in sys.argv:
    # Force offline mode during revision generation
    run_migrations_offline()
elif context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
