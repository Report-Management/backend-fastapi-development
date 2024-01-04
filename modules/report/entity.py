import uuid
from core import Base
from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import Column, String, DateTime, UUID, Integer, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from helper.date import format_relative_time
from modules.users.entity import UserEntity
from core.base import BaseRepo
from .model import ViewEnum
import datetime
import json

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
    spam = Column(Boolean, default=False)
    userID = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    
    reporter = relationship("UserEntity", back_populates="reports")

    @staticmethod
    def to_json(model: Base):
        report_dict = {
            "id": str(model.id),
            "category": model.category,
            "priority": model.priority,
            "reportedTime": model.reportedTime.isoformat(),
            "header": model.header,
            "information": model.information,
            "summary": model.summary,
            "photo": model.photo,
            "view": model.view,
            "approval": model.approval,
            "completed": model.completed,
            "spam": model.spam,
            "userID": str(model.userID)
        }
        return report_dict

    @staticmethod
    def to_model(model: Base, _user: UserEntity = None):
        report = {
            "id": str(model.id),
            "category": model.category,
            "priority": model.priority,
            "header": model.header,
            "information": model.information,
            "approval": model.approval,
            "view": model.view,
            "file": model.photo,
            "time": format_relative_time(model.reportedTime),
            "username": "Deleted Account" if _user is None else _user.username,
            "profile": "https://uazzhgvzukwpifcufyfg.supabase.co/storage/v1/object/public/profile/ee0da40e7d05f9c7fa31c693f2f21cec.jpg" if _user is None else _user.profilePhoto,
        }
        return report
