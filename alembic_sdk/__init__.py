from loguru import logger

from alembic_sdk.config import MIGRATIONS_DIR


def remove_migration_directory(directory_name=MIGRATIONS_DIR):
    """Remove an existing migration directory."""
    import os
    import shutil

    if os.path.isdir(directory_name):
        logger.debug(f"Removing migration directory at {directory_name}")
        shutil.rmtree(directory_name)
    else:
        logger.debug(f"No migration directory found at {directory_name}")


def remove_alembic_ini():
    """Remove an existing alembic.ini file."""
    import os

    if os.path.isfile("alembic.ini"):
        logger.debug("Removing alembic.ini file")
        os.remove("alembic.ini")
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

    # Initialize Alembic configuration
    alembic_config = Config()
    alembic_config.set_main_option("script_location", MIGRATIONS_DIR)
    alembic_config.config_file_name = "alembic.ini"  # Set the config file name

    # Create the Alembic environment
    logger.debug(f"Creating migration directory at {directory_name}")
    command.init(alembic_config, MIGRATIONS_DIR)


def create_engine(url, library="sqlalchemy"):
    """Create a database engine."""
    import importlib

    module = importlib.import_module(library)
    return module.create_engine(url)


def create_db(url, library="sqlalchemy"):
    """Create a database."""
    import importlib
    import os

    module = importlib.import_module(library)
    engine = module.create_engine(url)

    if url.startswith("sqlite:///"):
        # Create local folder for sqlite database
        folder_name = os.path.dirname(url).replace("sqlite:///", "")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

    if library == "sqlmodel":
        from sqlmodel import SQLModel

        SQLModel.metadata.create_all(engine)

    elif library == "sqlalchemy":
        from sqlalchemy import MetaData

        metadata = MetaData()
        metadata.create_all(engine)
