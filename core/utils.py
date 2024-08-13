import sys
import os
import uuid
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.routing import APIRoute
from typing import Type, TypeVar
from pydantic import UUID4, BaseModel
from sqlalchemy.orm import Session


load_dotenv()

def custom_generate_unique_id(route: APIRoute) -> str:
    # return f"{route.tags[0]}-{route.name}"
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"no-tag-{route.name}"


def env(var: str) -> any:
    """
        To get environment variable easily.

        Args:
            var (str): the environment variable.

        Returns:
            any: the value of the variable.

        Raises:
            ValueError: If variable not found in .env file.

        Example:
            >>> env("database_url")
            sqlite:///
    """
    return os.environ.get(var)

def gen_uuid() -> uuid:
    """
        To generate uuid for entity identification.

        Args:
            none

        Returns:
            UUID4: a uuid version 4.

        Example:
            >>> gen_uuid()
            73994a90-8762-478d-b041-7d1ccae7b9ad
    """
    return uuid.uuid4()




T = TypeVar('T', bound=BaseModel)
# Utility function to convert SQLAlchemy objects to Pydantic models.
def to_pydantic(db_object, pydantic_model: Type[T]) -> T:
    """
        To convert SQLALCHEMY ORM models to Pydantic models.

        Args:
            orm_object : the orm DB model.
            pydantic_model (BaseModel): the pydantic model.

        Returns:
            BaseModel: a pydantic model.

        Raises:
            ValueError: If model is not type BaseModel.

        Example:
            >>> to_pydantic(User, UserOut)
            
    """
    return pydantic_model(**db_object.__dict__)


