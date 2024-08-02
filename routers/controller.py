
from fastapi import APIRouter
from core.config import settings
from routers.v1 import *


router = APIRouter(prefix="/v1")


router.include_router(auth_router, tags=["Auth"]) 
router.include_router(user_router, prefix="/user", tags=["User"]) 