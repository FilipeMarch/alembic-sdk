from alembic_sdk import (
    create_db,
    create_engine,
    create_migration_directory,
    edit_env_py,
    remove_alembic_files,
)
from tests.utils import *

# logger.disable("alembic_sdk")


def delete_database_folder():
    """Delete the 'database' folder."""
    if os.path.isdir("database"):
        shutil.rmtree("database")


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

    # assert that 'sqlmodel' is in script.py.mako
    with open("alembic/script.py.mako", "r") as file:
        filedata = file.read()

    assert "import sqlmodel" in filedata

    # Create a new engine
    print(green + "Creating a new engine")
    engine = create_engine("sqlite:///database/database.db")

    assert engine != None

    # Create a new database using sqlmodel
    print(green + "Creating a new database using sqlmodel")
    create_db("sqlite:///database/database.db")

    assert os.path.isdir("database") == True
    assert os.path.isfile("database/database.db") == True

    # Edit the env.py file
    print(green + "Editing the env.py file")
    edit_env_py(
        url="sqlite:///database/database.db",
        import_models_file="tests/import_models.py",
    )

    delete_database_folder()

    # Remove the migration environment.
    print(red + "Removing alembic directory and alembic.ini file")
    remove_alembic_files()

    assert os.path.isdir("alembic") == False
