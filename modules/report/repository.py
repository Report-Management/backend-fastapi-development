from core import BaseRepo
from sqlalchemy import and_
from sqlalchemy.orm import Session
from .entity import ReportEntity
from .model import *
from fastapi import HTTPException, status
from sqlalchemy import UUID
from .summarize import text_summarization_bert
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
    

    @staticmethod
    def get_my_report(USERid: UUID, db: Session):
        reports = db.query(ReportEntity).filter(ReportEntity.userID == USERid).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Report with the USER {USERid} is not available")
        return reports
    

    @staticmethod
    def get_completed_report(db: Session):
        reports = db.query(ReportEntity).filter(ReportEntity.completed == True).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no completed reports")
        return reports
    

    @staticmethod
    def get_spam_report(db: Session):
        reports = db.query(ReportEntity).filter(ReportEntity.spam == True).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no spam reports")
        return reports
    

    @staticmethod
    def get_high_priority_report(db: Session):
        reports = db.query(ReportEntity).filter(and_(ReportEntity.priority == 'High', ReportEntity.spam == False)).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no high priority reports")
        return reports
    

    @staticmethod
    def get_medium_priority_report(db: Session):
        reports = db.query(ReportEntity).filter(and_(ReportEntity.priority == 'Medium', ReportEntity.spam == False)).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no medium priority reports")
        return reports
    

    @staticmethod
    def get_low_priority_report(db: Session):
        reports = db.query(ReportEntity).filter(and_(ReportEntity.priority == 'Low', ReportEntity.spam == False)).all()
        if not reports:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"There is no low priority reports")
        return reports
    

    @staticmethod
    def update_summary(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'summary': text_summarization_bert(report.first().information)})
        db.commit()
        return 'Updated summary successfully'


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
    def update_category(id: UUID, request: updateCategoryModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.category})
        db.commit()
        return 'Updated category successfully'
    

    @staticmethod
    def update_priority(id: UUID, request: updatePriorityModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.priority})
        db.commit()
        return 'Updated category successfully'
    

    @staticmethod
    def update_header(id: UUID, request: updateHeaderModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.header})
        db.commit()
        return 'Updated header successfully'


    @staticmethod
    def update_information(id: UUID, request: updateInformationModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.information})
        db.commit()
        return 'Updated information successfully'
    

    @staticmethod
    def update_view(id: UUID, request: updateViewModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.view})
        db.commit()
        return 'Updated view successfully'


    @staticmethod
    def mark_completed(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'completed': True})
        db.commit()
        return 'Mark completed successfully'
    

    @staticmethod
    def unmark_completed(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'completed': False})
        db.commit()
        return 'Unmark completed successfully'
    

    @staticmethod
    def mark_aprroved(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'approval': True})
        db.commit()
        return 'Mark approved successfully'
    

    @staticmethod
    def unmark_aprroved(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'approval': False})
        db.commit()
        return 'Unmark approved successfully'
    

    @staticmethod
    def mark_spam(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'spam': True})
        db.commit()
        return 'Mark spam successfully'
    

    @staticmethod
    def unmark_spam(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'spam': False})
        db.commit()
        return 'Unmark spam successfully'


    @staticmethod
    def remove(id: int, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.delete(synchronize_session=False)
        db.commit()
        return 'Deleted sucessfully'
