import uuid
from core import Base
from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import Column, String, DateTime, UUID, Integer, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class ReportEntity(Base):
    __tablename__ = 'reports'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(Enum('FacilityAndEnv', 'AdminstrativeAndStuffs', 'HealthAndSafety', 'BehavioralIssues', 'Academic', 'Community', 'SpecialRequest', 'Other', name='report_category'))
    priority = Column(Enum('Low', 'Medium', 'High', name='report_priority'))
    reportedTime = Column(DateTime, default=datetime.datetime.utcnow)
    header = Column(String)
    information = Column(String)
    summary = Column(String, default=None)
    photo = Column(String, default=None)
    view = Column(Enum('Public', 'Anonymous', name='report_view'))
    approval = Column(Boolean, default=False)
    completed = Column(Boolean, default=False)
    userID = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    reporter = relationship("UserEntity", back_populates="reports")