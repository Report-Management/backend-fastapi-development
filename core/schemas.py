from typing import Optional, TypeVar, Any, Generic, Annotated
from pydantic import BaseModel

T = TypeVar("T")

class ResponseSchema(BaseModel):
    code: int
    status: str
    message: Optional[str] = None
    result: Optional[Any] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
