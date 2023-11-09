from pydantic import BaseModel

class Report(BaseModel):
    category: str
    priority: str
    header: str
    information: str
    view: str
    spam: bool
    