from pydantic import BaseModel

class AccountModel(BaseModel):
    username: str
    email: str
    password: str
    