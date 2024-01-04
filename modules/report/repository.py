from core import BaseRepo, ResponseSchema, StatusEnum, SupabaseService
from sqlalchemy import and_, UUID, not_, or_, desc, asc
from sqlalchemy.sql.expression import false
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile, File
from typing import Dict, TypeVar
from datetime import datetime, timedelta
from modules.users.entity import UserEntity
from .summarize import summary_by_gemini
from .entity import ReportEntity
from .model import *
from .spam_detection import spam_or_ham
from helper.date import format_relative_time
import uuid
import json

class ReportRepository(BaseRepo):

    @staticmethod
    def get_all_reports(db: Session, filters: Dict[FilterEnum, Enum]):
        query = db.query(ReportEntity).filter(not_(ReportEntity.approval))
        for key, value in filters.items():
            if key == FilterEnum.Type:
                query = query.filter(ReportEntity.view == value.value)
            elif key == FilterEnum.Priority:
                priority = value.value
                query = query.filter(ReportEntity.priority == priority)
            elif key == FilterEnum.Category:
                category = value.value
                query = query.filter(ReportEntity.category == category)
            elif key == FilterEnum.Date:
                if value == DateEnum.Today:
                    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    today_end = today_start + timedelta(days=1)
                    query = query.filter(
                        and_(
                            ReportEntity.reportedTime >= today_start,
                            ReportEntity.reportedTime <= today_end
                        )
                    )
                elif value == DateEnum.Yesterday:
                    yesterday = datetime.now() - timedelta(days=1)
                    query = query.filter(ReportEntity.reportedTime == yesterday)

                elif value == DateEnum.LastMonth:
                    today = datetime.now()
                    last_month_start = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
                    last_month_end = last_month_start.replace(day=1) - timedelta(days=1)
                    query = query.filter(
                        and_(
                            ReportEntity.reportedTime >= last_month_start,
                            ReportEntity.reportedTime <= last_month_end
                            )
                    )

                elif value == DateEnum.LastYear:
                    today = datetime.now()
                    last_year_start = datetime(today.year - 1, 1, 1)
                    last_year_end = datetime(today.year - 1, 12, 31)
                    query = query.filter(
                        and_(
                            ReportEntity.reportedTime >= last_year_start,
                            ReportEntity.reportedTime <= last_year_end
                        )
                    )
        reports = query.order_by(desc(ReportEntity.reportedTime)).all()
        _list_report = [ReportEntity.to_model(report, _user=BaseRepo.get_by_id(db, UserEntity, report.userID)) for report in reports]
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=_list_report,
        )

    @staticmethod
    def get_all_approve_reports(db: Session):
        reports = db.query(ReportEntity).filter(
            and_(
                ReportEntity.approval,
                not_(ReportEntity.completed)
            )
        ).order_by(asc(ReportEntity.reportedTime)).all()
        _list_report = []
        for report in reports:
            _user: UserEntity = BaseRepo.get_by_id(db, UserEntity, report.userID)
            data = {
                "id": str(report.id),
                "category": report.category,
                "priority": report.priority,
                "header": report.header,
                "information": report.information,
                "approval": report.approval,
                "completed": report.completed,
                "view": report.view,
                "file": report.photo,
                "time": format_relative_time(report.reportedTime),
                "username": (
                    "Deleted Account"
                    if _user is None
                    else _user.username
                    if report.view == ViewEnum.Public.value
                    else ViewEnum.Anonymous.value
                ),
                "profile": (
                    "https://uazzhgvzukwpifcufyfg.supabase.co/storage/v1/object/public/profile/ee0da40e7d05f9c7fa31c693f2f21cec.jpg"
                    if _user is None
                    else _user.profilePhoto
                    if report.view == ViewEnum.Public.value
                    else "https://uazzhgvzukwpifcufyfg.supabase.co/storage/v1/object/public/profile/anonymous-man.png?t=2024-01-04T16%3A21%3A53.553Z"
                ),
            }
            _list_report.append(data)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=_list_report
        )

    @staticmethod
    def get_report(id: str, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id).first()
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No found report_id: {id}")
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=ReportEntity.to_json(report)
        )

    @staticmethod
    def get_my_report(USERid: UUID, db: Session):
        reports = db.query(ReportEntity).filter(ReportEntity.userID == USERid).order_by(asc(ReportEntity.reportedTime)).all()

        if not reports:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report with the USER {USERid} is not available")
        _list_report = [ReportEntity.to_model(report, _user=BaseRepo.get_by_id(db, UserEntity, report.userID)) for report in reports]
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=_list_report
        )

    @staticmethod
    def get_completed_report(db: Session):
        reports = db.query(ReportEntity).filter(
            and_(
                ReportEntity.completed,
                ReportEntity.approval
            )
        ).order_by(asc(ReportEntity.reportedTime)).all()
        _list_report = []
        for report in reports:
            _user: UserEntity = BaseRepo.get_by_id(db, UserEntity, report.userID)
            data = {
                "id": str(report.id),
                "category": report.category,
                "priority": report.priority,
                "header": report.header,
                "information": report.information,
                "completed": report.completed,
                "view": report.view,
                "file": report.photo,
                "time": format_relative_time(report.reportedTime),
                "username": "Deleted Account" if _user is None else _user.username,
                "profile": "https://uazzhgvzukwpifcufyfg.supabase.co/storage/v1/object/public/profile/ee0da40e7d05f9c7fa31c693f2f21cec.jpg" if _user is None else _user.profilePhoto,
            }
            _list_report.append(data)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=_list_report,
        )

    @staticmethod
    def get_spam_report(db: Session):
        reports = db.query(ReportEntity).filter(ReportEntity.spam).order_by(asc(ReportEntity.reportedTime)).all()
        _list_report = []
        for report in reports:
            _user: UserEntity = BaseRepo.get_by_id(db, UserEntity, report.userID)
            data = {
                "id": str(report.id),
                "category": report.category,
                "priority": report.priority,
                "header": report.header,
                "information": report.information,
                "spam": report.spam,
                "view": report.view,
                "file": report.photo,
                "time": format_relative_time(report.reportedTime),
                "username": "Deleted Account" if _user is None else _user.username,
                "profile": "https://uazzhgvzukwpifcufyfg.supabase.co/storage/v1/object/public/profile/ee0da40e7d05f9c7fa31c693f2f21cec.jpg" if _user is None else _user.profilePhoto,
            }
            _list_report.append(data)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=_list_report,
        )

    @staticmethod
    def search_report(search: str, db: Session):
        reports = db.query(ReportEntity).filter(
            and_(
                or_(
                    ReportEntity.header.like(f"%{search}%"),
                    ReportEntity.information.like(f"%{search}%")
                ),
                ReportEntity.approval
            )
        ).order_by(desc(ReportEntity.reportedTime)).all()
        _list_report = [ReportEntity.to_model(report, _user=BaseRepo.get_by_id(db, UserEntity, report.userID)) for report in reports]
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=_list_report,
        )

    @staticmethod
    def create(request: CreateReportModel, db: Session, user_id: UUID):
        new_report = ReportEntity(
            id=request.id,
            category=request.category,
            priority=request.priority,
            header=request.header,
            information=request.information,
            view=request.view,
            photo=request.file,
            spam=spam_or_ham(request.information),
            userID=user_id
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Report create successfully"
        )

    @staticmethod
    def update_summary_report(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id).first()
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')


        if report.summary is None:
            summary_text = None
            print(summary_text)
            report.summary = summary_text
            db.commit()

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            result=report.summary
        )


    @staticmethod
    def update_report(id: UUID, request: UpdateReportModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.category, 'priority': request.priority, 'header': request.header,
                       'information': request.information, 'view': request.view})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update successfully"
        )

    @staticmethod
    def update_category(id: UUID, request: CategoryEnum, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'category': request.value})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update successfully"
        )

    @staticmethod
    def update_priority(id: UUID, request: PriorityEnum, db: Session):
        print(request.value)
        print(id)
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'priority': request.value})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update successfully"
        )

    @staticmethod
    def update_header(id: UUID, request: UpdateHeaderModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'header': request.header})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update successfully"
        )

    @staticmethod
    def update_information(id: UUID, request: UpdateInformationModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'information': request.information})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update successfully"
        )

    @staticmethod
    def update_view(id: UUID, request: UpdateViewModel, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'view': request.view})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update successfully"
        )

    @staticmethod
    def mark_completed(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'completed': True})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Completed"
        )

    @staticmethod
    def unmark_completed(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'completed': False})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message='Unmark completed'
        )

    @staticmethod
    def mark_approved(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'approval': True})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message='Approved'
        )

    @staticmethod
    def unmark_approved(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'approval': False})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message='Unmark approved'
        )

    @staticmethod
    def mark_spam(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'spam': True})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message='Mark spam'
        )

    @staticmethod
    def unmark_spam(id: UUID, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.update({'spam': False})
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message='Unmark spam'
        )

    @staticmethod
    def update_file(id: str, file: UploadFile, db):
        bucket = 'testbucket'
        print(SupabaseService.is_file_exist(bucket, id))
        if SupabaseService.is_file_exist(bucket, id):
            is_deleted = SupabaseService.delete_image(bucket, id)
            if is_deleted:
                _url = SupabaseService.upload_file(bucket, file, id)
                if _url:
                    report = db.query(ReportEntity).filter(ReportEntity.id == id)
                    if not report.first():
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
                    report.update({'photo': _url})
                    db.commit()
                    return ResponseSchema(
                        code=status.HTTP_200_OK,
                        status=StatusEnum.Success.value,
                        message='Updated Successfully'
                    )
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Fail upload')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Fail remove')
        else:
            _url = SupabaseService.upload_file(bucket, file, id)
            print(_url)
            if _url:
                report = db.query(ReportEntity).filter(ReportEntity.id == id)
                if not report.first():
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
                report.update({'photo': _url})
                db.commit()
                return ResponseSchema(
                    code=status.HTTP_200_OK,
                    status=StatusEnum.Success.value,
                    message='Updated Successfully'
                )
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Fail upload')

    @staticmethod
    def remove_file(id: str, db: Session):
        bucket = 'testbucket'
        print(SupabaseService.is_file_exist(bucket, id))
        if SupabaseService.is_file_exist(bucket, id):
            is_deleted = SupabaseService.delete_image(bucket, id)
            if is_deleted:
                report = db.query(ReportEntity).filter(ReportEntity.id == id)
                if not report.first():
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
                report.update({'photo': None})
                db.commit()
                return ResponseSchema(
                    code=status.HTTP_200_OK,
                    status=StatusEnum.Success.value,
                    message='Remove Successfully'
                )
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Fail remove')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Not Found')

    @staticmethod
    def remove(id: str, db: Session):
        report = db.query(ReportEntity).filter(ReportEntity.id == id)
        if not report.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Report with id {id} not found')
        report.delete(synchronize_session=False)
        db.commit()
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message='Delete Successfully'
        )
