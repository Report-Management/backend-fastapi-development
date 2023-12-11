from pydantic import BaseModel
from enum import Enum
class UserModel(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserLoginModel(BaseModel):
    email: str
    password: str


class UserEnum(Enum):
    Admin = 'Admin'
    Normal = 'User'
