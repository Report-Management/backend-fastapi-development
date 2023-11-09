from pydantic import BaseModel

class Account(BaseModel):
    username: str
    email: str
    password: str
    