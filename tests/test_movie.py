
from test_main import client, setup_database, pytest


@pytest.mark.parametrize("title, description", [("Gladiator", "Lorem Ipsum")])
def test_add_movie(client, setup_database, title, description, ver):
    # get token from temp file
    with open("tests/test_token.txt", "r") as f:
        token = f.read().strip()

    response = client.post(f"{ver}/movie", 
                           json={"title": title, "description": description}, 
                           headers={"Authorization": f"Bearer {token}"}
                           )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Movie Added"
    assert data['data']['title'] == "Gladiator"    
    # write created movie id to temp file
    with open("tests/test_movie.txt", "w") as f:
        f.write(data['data']['muid'])


def test_get_movies(client, ver):
    response = client.get(f"{ver}/movie")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Success"    
    assert isinstance(data['data'] , list)
    
def test_get_movie(client, ver):
    # get movie from temp file
    with open("tests/test_movie.txt", "r") as f:
        movie_id = f.read().strip()

    response = client.get(f"{ver}/movie/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Success"    
    assert isinstance(data['data'] , dict)
    assert data['data']['title'] == "Gladiator" 


def test_update_movie(client, ver):
    # get token from temp file
    with open("tests/test_token.txt", "r") as f:
        token = f.read().strip()
    # get movie from temp file
    with open("tests/test_movie.txt", "r") as f:
        movie_id = f.read().strip()

    response = client.put(f"{ver}/movie/{movie_id}", 
                           json={"title": "Gladiator Part 2", "description": "Updated Lorem Ipsum"}, 
                           headers={"Authorization": f"Bearer {token}"}
                           )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie Updated"    
    assert isinstance(data['data'] , dict)
    assert data['data']['title'] == "Gladiator Part 2" 
    assert movie_id == data['data']['muid']


def test_delete_movie(client, ver):
    # get token from temp file
    with open("tests/test_token.txt", "r") as f:
        token = f.read().strip()
    # get movie from temp file
    with open("tests/test_movie.txt", "r") as f:
        movie_id = f.read().strip()

    response = client.delete(f"{ver}/movie/{movie_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie Deleted" 