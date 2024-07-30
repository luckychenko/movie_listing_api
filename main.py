

# Add the project root to the sys.path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from middleware import movie_middleware
from logger import logger

from core.database import Base, engine
from core.utils import custom_generate_unique_id, env
from routers.auth import auth_router


Base.metadata.create_all(bind=engine)




app = FastAPI(
    title=env('PROJECT_NAME'),
    openapi_url=f"{env('API_VERSION_STR')}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    ) 

app.add_middleware(BaseHTTPMiddleware, dispatch=movie_middleware)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        str(origin).strip("/") for origin in env('CORS') 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

logger.info("starting app")

app.include_router(auth_router, prefix=env('API_VERSION_STR')) 



@app.get('/')
def index():
    return {'message': 'This is a Movie Listing App'}