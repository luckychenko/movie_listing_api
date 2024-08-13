
from fastapi import APIRouter
from routers.v1 import *


routerv1 = APIRouter(prefix="/v1")


routerv1.include_router(auth_router, tags=["Auth"]) 
routerv1.include_router(movie_router, prefix="/movie", tags=["Movie"]) 
routerv1.include_router(rating_router, prefix="/rate", tags=["Movie Rating"]) 
routerv1.include_router(comment_router, prefix="/comment", tags=["Movie Comment"]) 