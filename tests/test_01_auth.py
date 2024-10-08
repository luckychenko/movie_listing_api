
from test_main import client, setup_database, pytest




def test_home(client, ver):
    response = client.get("/")
    assert response.status_code == 200
    # data = response.json()

@pytest.mark.parametrize("email, password, full_name", [("testuser@gmail.com", "testpassword", "Test User")])
def test_signup(client, setup_database, email, password, full_name, ver):
    response = client.post(f"{ver}/signup", json={"email": email, "full_name": full_name, "password": password})
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["email"] == email

@pytest.mark.parametrize("email, password", [("testuser@gmail.com", "testpassword")])
def test_login(client, setup_database, email, password, ver):
    # # First, sign up the user
    # response = client.post(f"{ver}/signup", json={"email": email, "full_name": full_name, "password": password})
    # assert response.status_code == 201

    # Then, log in the user
    response = client.post(f"{ver}/login", data={"username": email, "password": password})
    assert response.status_code == 200
    data = response.json()
    token = data['access_token']
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    # write token to temp file
    with open("tests/test_token.txt", "w") as f:
        f.write(token)
