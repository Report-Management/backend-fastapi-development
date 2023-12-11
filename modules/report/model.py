from pydantic import BaseModel, UUID4
from enum import Enum
from typing import Optional, Annotated
from fastapi import Form, UploadFile, File

class CreateReportModel(BaseModel):
    id: UUID4
    category: str
    priority: str
    header: str
    information: str
    view: str
    file: Optional[str] = None

class UpdateReportModel(BaseModel):
    category: str
    priority: str
    header: str
    information: str
    view: str

class UpdateCategoryModel(BaseModel):
    category: str

class UpdatePriorityModel(BaseModel):
    priority: str

class UpdateHeaderModel(BaseModel):
    header: str

class UpdateInformationModel(BaseModel):
    information: str

class UpdateViewModel(BaseModel):
    view: str

class FilterEnum(Enum):
    Type = "type"
    Priority = "priority"
    Category = "category"
    Date = "date"

class PriorityEnum(Enum):
    Low = 'Low'
    Medium = 'Medium'
    High = 'High'

class CategoryEnum(Enum):
    FacilityAndEnv = 'FacilityAndEnv'
    AdminstrativeAndStuffs = 'AdminstrativeAndStuffs'
    HealthAndSafety = 'HealthAndSafety'
    BehavioralIssues = 'BehavioralIssues'
    Academic = 'Academic'
    Community = 'Community'
    SpecialRequest = 'SpecialRequest'
    Other = 'Other'

class DateEnum(Enum):
    Today = 'today'
    Yesterday = 'yesterday'
    LastMonth = 'lastmonth'
    LastYear = 'lastyear'

class TypeEnum(Enum):
    Approved = 'approved'
    NotApproved = 'notapproved'

class ViewEnum(Enum):
    Public = 'Public'
    Anonymous = 'Anonymous'


class CreateReportModelV2(BaseModel):
    id: UUID4
    category: Annotated[CategoryEnum, Form()]
    priority: Annotated[PriorityEnum, Form()]
    header: Annotated[str, Form()]
    information: Annotated[str, Form()]
    view: Annotated[ViewEnum, Form()]
    file: UploadFile = File(None),