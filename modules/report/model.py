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


class updateCategoryModel(BaseModel):
    category: str


class updatePriorityModel(BaseModel):
    priority: str


class updateHeaderModel(BaseModel):
    header: str


class updateInformationModel(BaseModel):
    information: str


class updateViewModel(BaseModel):
    view: str
