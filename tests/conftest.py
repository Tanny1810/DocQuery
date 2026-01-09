# tests/conftest.py
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure top-level packages (`app`, `shared`, `worker`) are importable from tests
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(BASE_DIR, "api"))
sys.path.insert(0, os.path.join(BASE_DIR, "shared"))

import importlib.util

# Load `Base` directly from the api/app/models/base.py file to avoid package name issues
base_path = os.path.join(BASE_DIR, "api", "app", "models", "base.py")
spec = importlib.util.spec_from_file_location("app.models.base", base_path)
base_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_module)
Base = base_module.Base

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/docquery_test"
)


@pytest.fixture(scope="session")
def engine():
    # Only run DB fixtures in CI or when explicitly enabled.
    if not os.getenv("CI") and not os.getenv("RUN_DB_TESTS"):
        pytest.skip(
            "Skipping DB tests outside CI or without RUN_DB_TESTS",
            allow_module_level=True,
        )

    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
