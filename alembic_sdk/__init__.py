from loguru import logger

from alembic_sdk.config import MIGRATIONS_DIR


def remove_migration_directory(directory_name=MIGRATIONS_DIR):
    """Remove an existing migration directory."""
    import os
    import shutil

    if os.path.isdir(directory_name):
        logger.debug(f"Removing migration directory at {directory_name}")
        shutil.rmtree(directory_name)
        logger.debug(f"Removed migration directory at {directory_name}")
    else:
        logger.debug(f"No migration directory found at {directory_name}")


def remove_alembic_ini():
    """Remove an existing alembic.ini file."""
    import os

    if os.path.isfile("alembic.ini"):
        logger.debug("Removing alembic.ini file")
        os.remove("alembic.ini")
        logger.debug("Removed alembic.ini file")
    else:
        logger.debug("No alembic.ini file found")


def remove_alembic_files():
    """Remove an existing alembic.ini file and migration directory."""
    remove_migration_directory()
    remove_alembic_ini()


def create_migration_directory(directory_name=MIGRATIONS_DIR):
    """Create a new migration directory."""
    from alembic import command
    from alembic.config import Config

    # Set your database connection string
    database_url = "sqlite:///example.db"

    # Initialize Alembic configuration
    alembic_config = Config()
    alembic_config.set_main_option("script_location", MIGRATIONS_DIR)
    alembic_config.set_main_option("sqlalchemy.url", database_url)
    alembic_config.config_file_name = "alembic.ini"  # Set the config file name

    # Create the Alembic environment
    command.init(alembic_config, MIGRATIONS_DIR)

    logger.debug(f"Created new migration directory at {directory_name}")
