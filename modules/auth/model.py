from enum import Enum
from pydantic import BaseModel

class AccountType(Enum):
    ADMIN = "Admin"
    USER = "User"


class EmailModel(BaseModel):
    email: str

class ForgetPasswordModel(BaseModel):
    password: str