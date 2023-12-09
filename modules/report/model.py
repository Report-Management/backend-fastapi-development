from pydantic import BaseModel
from enum import Enum

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


class createReportWithFileModel(BaseModel):
    id: str
    category: str
    priority: str
    header: str
    information: str
    photo: str
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
