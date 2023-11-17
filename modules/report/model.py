from pydantic import BaseModel


class createReportModel(BaseModel):
    category: str
    priority: str
    header: str
    information: str
    view: str
    spam: bool


class updateReportModel(BaseModel):
    category: str
    priority: str
    header: str
    information: str
    view: str  
