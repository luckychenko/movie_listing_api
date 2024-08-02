import sys
import os
import uuid
from dotenv import load_dotenv
from fastapi.routing import APIRoute

load_dotenv()

def custom_generate_unique_id(route: APIRoute) -> str:
    # return f"{route.tags[0]}-{route.name}"
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    else:
        return f"no-tag-{route.name}"


def env(var: str) -> any:
    return os.environ.get(var)

def gen_uuid() -> uuid:
    return uuid.uuid4()