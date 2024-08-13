import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from core.config import settings
from core.database import Base, get_db
from main import app



engine = create_engine(settings.TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # delete the temp files created while running tests
    if os.path.exists("tests/test_token.txt"):
        os.remove("tests/test_token.txt")
    if os.path.exists("tests/test_movie.txt"):
        os.remove("tests/test_movie.txt")



