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


class showReportModel(BaseModel):
    id : str
    category: str
    priority: str
    reportedTime: str
    header: str
    information: str
    view: str
    summary: str
    photo: str
    view: str
    approval: bool
    completed: bool
    spam: bool
    userID: str
