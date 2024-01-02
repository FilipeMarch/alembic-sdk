from alembic_sdk import (
    create_db,
    create_engine,
    create_migration_directory,
    remove_alembic_files,
)
from tests.utils import *

# logger.disable("alembic_sdk")


def test_alembic_sdk(environment):
    """
    The main function that is called when pytest is run.
    """
    print("\n", yellow + ">>> :+: Testing alembic sdk :+: <<<\n")

    # Remove the migration environment.
    print(red + "Removing alembic directory and alembic.ini file")
    remove_alembic_files()

    assert os.path.isdir("alembic") == False

    # Create a new migration directory.
    print(green + "Creating alembic directory")
    create_migration_directory()

    assert os.path.isdir("alembic") == True
    assert os.path.isfile("alembic.ini") == True

    # Remove the migration environment.
    print(red + "Removing alembic directory and alembic.ini file")
    remove_alembic_files()

    assert os.path.isdir("alembic") == False

    # Create a new engine
    print(green + "Creating a new engine")
    engine = create_engine("sqlite:///database/database.db")

    assert engine != None

    # Delete the 'database' folder
    if os.path.isdir("database"):
        shutil.rmtree("database")

    # Create a new database using sqlalchemy
    print(green + "Creating a new database using sqlalchemy")
    create_db("sqlite:///database/database.db")

    assert os.path.isdir("database") == True
    assert os.path.isfile("database/database.db") == True

    # Delete the 'database' folder
    if os.path.isdir("database"):
        shutil.rmtree("database")

    # Create a new database using sqlmodel
    print(green + "Creating a new database using sqlmodel")
    create_db("sqlite:///database/database.db", library="sqlmodel")

    assert os.path.isdir("database") == True
    assert os.path.isfile("database/database.db") == True
