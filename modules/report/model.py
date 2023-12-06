from pydantic import BaseModel
from enum import Enum

class PriorityEnum(Enum):
    Low = 'Low'
    Medium = 'Medium'
    High = 'High'


class createReportModel(BaseModel):
    id: str
    category: str
    priority: str
    header: str
    information: str
    view: str


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
