import os
import shutil
import time

from loguru import logger

logger.add(
    "logs/alembic_sdk.log",
    rotation="5 MB",
    retention="10 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
)


import pytest
from colorama import Fore, Style, init
from icecream import ic

red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
init(autoreset=True)


def delete_alembic_folder():
    if os.path.exists("alembic"):
        shutil.rmtree("alembic")


def delete_alembic_ini():
    if os.path.exists("alembic.ini"):
        os.remove("alembic.ini")


@pytest.fixture()
def environment():
    delete_alembic_folder()
    delete_alembic_ini()
    yield
