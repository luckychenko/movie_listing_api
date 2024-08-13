
from routers.v1.auth_route import auth_router
from routers.v1.movie_route import movie_router
from routers.v1.rating_route import rating_router 
from routers.v1.comment_route import comment_router 

__all__ = ["auth_router", "movie_router", "rating_router", "comment_router"]