from core import BaseRepo
from sqlalchemy.orm import Session
from typing import Generic, TypeVar
from .entity import Report as ReportEntity
from .model import Report

T = TypeVar('T')

class ReportRepo(BaseRepo):
    def create(request: Report, db: Session):
        new_report = ReportEntity(category=request.category, priority=request.priority, header=request.header, information=request.information, view=request.view, spam=request.spam, accountID=1)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
