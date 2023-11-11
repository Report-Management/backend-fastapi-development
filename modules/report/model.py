from pydantic import BaseModel

class ReportModel(BaseModel):
    category: str
    priority: str
    header: str
    information: str
    view: str
    spam: bool
    