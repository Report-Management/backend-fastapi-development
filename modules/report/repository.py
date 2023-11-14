from core import BaseRepo
from sqlalchemy.orm import Session
from .entity import ReportEntity
from .model import ReportModel

class ReportRepository(BaseRepo):

    @staticmethod
    def create(request: ReportModel, db: Session):
        new_report = ReportEntity(category=request.category, priority=request.priority, header=request.header, information=request.information, view=request.view, spam=request.spam, accountID=1)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
