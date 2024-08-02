import sys
import os

# Add the project root to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from middleware import movie_middleware
from logger import logger

from core.config import settings
from core.database import Base, engine
from core.utils import custom_generate_unique_id
from routers.controller import router

from models import *

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_VERSION_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    ) 

# # middleware for logging
# app.add_middleware(BaseHTTPMiddleware, dispatch=movie_middleware)

# # Set all CORS enabled origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         str(origin).strip("/") for origin in settings.CORS 
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],  
# )

# logger.info("starting app")

app.include_router(router, prefix='/api') 



@app.get('/')
def index():
    return {'message': 'This is a Movie Listing App'}