
from test_main import client, setup_database, pytest


def test_add_comment(client, setup_database, ver):
    # get token from temp file
    with open("tests/test_token.txt", "r") as f:
        token = f.read().strip()

    # get movie from temp file
    with open("tests/test_movie.txt", "r") as f:
        movie_id = f.read().strip()

    # test comment on movie
    response = client.post(f"{ver}/comment", 
                           json={"content": 'A test comment for the movie', "movie_id": movie_id}, 
                           headers={"Authorization": f"Bearer {token}"}
                           )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Comment Added"
    assert "content" in data['data']
 

def test_get_comments(client, ver):
    # get movie from temp file
    with open("tests/test_movie.txt", "r") as f:
        movie_id = f.read().strip()

    response = client.get(f"{ver}/comment/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Success"  
    assert "content" in data['data'][0]  
    assert isinstance(data['data'] , list)


