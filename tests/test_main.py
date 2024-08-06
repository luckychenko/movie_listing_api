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

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)




# @pytest.mark.parametrize("email, password", [("testuser", "testpassword")])
# def test_get_books(client, setup_database, email, password):
#     response = client.post("/login", data={"email": email, "password": password})
#     assert response.status_code == 200
#     token = response.json()["access_token"]

#     # Then, get the books
#     response = client.get("/books/")
#     assert response.status_code == 401
#     response = client.get("/books/", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     data = response.json()
#     assert "data" in data

# @pytest.mark.parametrize("email, password", [("testuser", "testpassword")])
# def test_create_book(client, setup_database, email, password):
#     response = client.post("/login", data={"email": email, "password": password})
#     assert response.status_code == 200
#     token = response.json()["access_token"]

#     # Then, create a book
#     book_data = {"title": "Test Book", "author": "Test Author", "description": "A good book"}
#     response = client.post("/books", json=book_data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["message"] == "success"
#     assert data['data']['title'] == "Test Book"