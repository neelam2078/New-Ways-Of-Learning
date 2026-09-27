import os
import tempfile
from pathlib import Path


TEST_DATABASE = (
    Path(tempfile.gettempdir())
    / "pocketsmart_test.db"
)


if TEST_DATABASE.exists():
    TEST_DATABASE.unlink()


os.environ[
    "DATABASE_URL"
] = f"sqlite:///{TEST_DATABASE}"


os.environ[
    "SECRET_KEY"
] = "test-secret-key"


os.environ[
    "GEMINI_API_KEY"
] = ""


from app.main import app
from app.database import init_db

from fastapi.testclient import TestClient

import pytest


@pytest.fixture(
    scope="session"
)
def client():

    init_db()

    with TestClient(app) as test_client:

        yield test_client