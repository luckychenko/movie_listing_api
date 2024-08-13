
from test_main import client, setup_database, pytest


def test_rate_movie(client, setup_database, ver):
    # get token from temp file
    with open("tests/test_token.txt", "r") as f:
        token = f.read().strip()

    # will create a movie first so endpoint can use the movie to test 

    # dummy movie data for other tests
    response = client.post(f"{ver}/movie", 
                           json={"title": "Oliver Twist", "description": "Lorem Ipsum"}, 
                           headers={"Authorization": f"Bearer {token}"}
                           )
    
    movie_id = response.json()['data']['muid']
    response = client.post(f"{ver}/rate", 
                           json={"score": 7.5,  "movie_id": movie_id}, 
                           headers={"Authorization": f"Bearer {token}"}
                           )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Movie Rated"
    assert "ruid" in data ['data'] 
       
    # write created movie id to temp file
    with open("tests/test_movie.txt", "w") as f:
        f.write(movie_id) 


def test_get_ratings(client, ver):
    # get movie from temp file
    with open("tests/test_movie.txt", "r") as f:
        movie_id = f.read().strip()

    response = client.get(f"{ver}/rate/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Success"  
    assert "avg_ratings_score" in data ['data']  


