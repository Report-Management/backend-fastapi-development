from core import BaseRepo
from sqlalchemy.orm import Session
from .entity import ReportEntity
from .model import createReportModel, updateReportModel
from fastapi import HTTPException, status
from sqlalchemy import UUID
import uuid

class ReportRepository(BaseRepo):


    @staticmethod
    def get_all_reports(db: Session):
        reports = db.query(ReportEntity).all()
        return reports


    @staticmethod
    def get_report(id: str, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id).first()
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Report with the {id} is not available")
        return report
    

    def get_my_report(USERid: UUID, db: Session):
        reports = db.query(ReportEntity).filter(ReportEntity.userID == USERid).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Report with the USER {USERid} is not available")
        return reports
    

    @staticmethod
    def create(request: createReportModel, db: Session, USERid: UUID):
        new_report = ReportEntity(
            id=uuid.uuid4(),
            category=request.category, priority=request.priority, header=request.header, information=request.information, view=request.view, spam=request.spam, userID=USERid)
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report


    @staticmethod
    def update(id: UUID, request: updateReportModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category':request.category, 'priority':request.priority, 'header':request.header, 'information':request.information, 'view':request.view})
        db.commit()
        return 'Updated successfully'
    

    @staticmethod
    def mark_completed(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'completed': True})
        db.commit()
        return 'Mark completed successfully'
    

    @staticmethod
    def mark_aprroved(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'approval': True})
        db.commit()
        return 'Mark approved successfully'


    @staticmethod
    def remove(id: int, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.delete(synchronize_session=False)
        db.commit()
        return 'Deleted sucessfully'
