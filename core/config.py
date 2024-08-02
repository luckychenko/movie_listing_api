from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_VERSION_STR: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SENTRY_DSN: HttpUrl 
    JWT_ALGORITHM: str
    DATABASE_URL: str 
    CORS: str
 
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings() 
 