
from fastapi import APIRouter
from routers.v1 import *


routerv1 = APIRouter(prefix="/v1")


routerv1.include_router(auth_router, tags=["Auth"]) 
routerv1.include_router(user_router, prefix="/user", tags=["User"]) 