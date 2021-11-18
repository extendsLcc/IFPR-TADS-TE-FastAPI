import os

DATABASE_URL = 'sqlite:///testdb.sqlite'
os.environ["DATABASE_URL"] = DATABASE_URL
os.environ["TEST_DATABASE"] = 'true'

from typing import Generator
from fastapi.testclient import TestClient
import pytest
from main import app
from migrate_tables import migrate_refresh_database


@pytest.fixture(scope="function")
def client() -> Generator:
    migrate_refresh_database(DATABASE_URL)
    with TestClient(app) as client:
        yield client