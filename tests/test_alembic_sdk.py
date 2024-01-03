from alembic_sdk import (
    create_db,
    create_engine,
    create_migration_directory,
    edit_env_py,
    generate_revision,
    remove_alembic_files,
    upgrade_head,
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
    print(red + "Creating alembic directory")
    create_migration_directory()

    assert os.path.isdir("alembic") == True
    assert os.path.isfile("alembic.ini") == True

    # assert that 'sqlmodel' is in script.py.mako
    with open("alembic/script.py.mako", "r") as file:
        filedata = file.read()

    assert "import sqlmodel" in filedata

    # Create a new engine
    print(red + "Creating a new engine")
    engine = create_engine("sqlite:///database/database.db")

    assert engine != None

    # Create a new database using sqlmodel
    print(red + "Creating a new database using sqlmodel")
    create_db("sqlite:///database/database.db")

    assert os.path.isdir("database") == True
    assert os.path.isfile("database/database.db") == True
    assert os.path.getsize("database/database.db") == 0

    # Edit the env.py file
    print(red + "Editing the env.py file")
    edit_env_py(
        url="sqlite:///database/database.db",
        import_models_file="tests/import_models_1.py",
    )

    # Generate a new revision
    print(red + "Generating a new revision")
    revision_success = generate_revision()

    # assert that the revision file was created
    assert any(
        f.endswith("v1.py") for f in os.listdir("alembic/versions")
    ), "v1.py was not created"
    assert revision_success == True
    assert os.path.getsize("database/database.db") != 0

    # Try to generate a new revision again and assert that it fails
    print(red + "Trying to generate a new revision again")
    revision_success = generate_revision()

    assert revision_success == False

    # Executing alembic upgrade head
    print(red + "Alembic upgrade head")
    upgrade_success = upgrade_head()

    assert upgrade_success == True

    # Edit the env.py file
    print(red + "Editing the env.py file")
    edit_env_py(
        url="sqlite:///database/database.db",
        import_models_file="tests/import_models_2.py",
    )

    # Delete __pycache__ folders
    print(red + "Deleting __pycache__ folders")

    def delete_pycache_folders():
        for root, dirs, files in os.walk(".", topdown=False):
            for name in dirs:
                if name == "__pycache__":
                    shutil.rmtree(os.path.join(root, name))

    delete_pycache_folders()

    # Generate a new revision
    print(red + "Generating a new revision")
    revision_success = generate_revision()

    # assert that the revision file was created
    assert any(
        f.endswith("v2.py") for f in os.listdir("alembic/versions")
    ), "v2.py was not created"
    assert revision_success == True

    # Executing alembic upgrade head
    print(red + "Alembic upgrade head")
    upgrade_success = upgrade_head()

    # Remove the migration environment.
    print(red + "Removing alembic directory and alembic.ini file")
    remove_alembic_files()
    delete_database_folder()

    assert os.path.isdir("alembic") == False
