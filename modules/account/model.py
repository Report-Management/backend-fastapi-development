from pydantic import BaseModel

class Account(BaseModel):
    username: str
    email: str
    password: str

    class Config():
        from_attributes = True