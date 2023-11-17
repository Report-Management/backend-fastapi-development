from core import BaseRepo
from sqlalchemy.orm import Session
from .entity import ReportEntity
from .model import ReportModel
from fastapi import HTTPException, status
from sqlalchemy import UUID
import uuid

class ReportRepository(BaseRepo):

    @staticmethod
    def create(request: ReportModel, db: Session, id: UUID):
        new_report = ReportEntity(
            id=uuid.uuid4(),
            category=request.category, 
            priority=request.priority, header=request.header, information=request.information, view=request.view, spam=request.spam, userID=id)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report
    
    @staticmethod
    def remove(id: int, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.delete(synchronize_session=False)
        db.commit()
        return 'Deleted sucessfully'
    
    @staticmethod
    def update(id: int, request: ReportModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category':request.category, 'priority':request.priority, 'header':request.header, 'information':request.information, 'view':request.view})
        db.commit()
        return 'Updated successfully'
