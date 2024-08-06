from typing import Optional

from pydantic import BaseModel


class ResponseBase(BaseModel):
    """
        Represents a base response in the system.

        Attributes:
            message (Optional[str]): The message sent to frontend.
            has error (Optional[bool]): A boolean to signify error.
            error (Optional[str]): A message describing the error, if any.
    """
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None