import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import *
from .repository import ReportRepository
from sqlalchemy import UUID

router = APIRouter(
    prefix="/Report",
    tags=['Reports'],
    responses={422: {"description": "Validation Error"}},
)


@router.get('/show', summary=None, name='SHOW_ALL', operation_id='get_all_reports')
def get_all_reports(db: Session = Depends(get_db)):
    return ReportRepository.get_all_reports(db)


@router.get('/show/{id}', summary=None, name='SHOW', operation_id='get_report')
def get_report(id: str, db: Session = Depends(get_db)):
    return ReportRepository.get_report(id, db)


@router.get('/showMyReport', summary=None, name='SHOW_MY_REPORT', operation_id='get_my_report')
def get_my_report(USERid: UUID = Depends(JWTBearer()), db: Session = Depends(get_db)):
    return ReportRepository.get_my_report(JWTRepo.decode_token(USERid), db)


@router.get('/showCompletedReport', summary=None, name='SHOW_COMPLETED_REPORT', operation_id='get_completed_report')
def get_my_report(db: Session = Depends(get_db)):
    return ReportRepository.get_completed_report(db)


@router.get('/showSpamReport', summary=None, name='SHOW_SPAM_REPORT', operation_id='get_spam_report')
def get_spam_report(db: Session = Depends(get_db)):
    return ReportRepository.get_spam_report(db)


@router.get('/showHighPriorityReport', summary=None, name='SHOW_HIGH_PRIORITY_REPORT', operation_id='get_high_priority_report')
def get_my_report(db: Session = Depends(get_db)):
    return ReportRepository.get_high_priority_report(db)


@router.get('/showMediumPriorityReport', summary=None, name='SHOW_MEDIUM_PRIORITY_REPORT', operation_id='get_medium_priority_report')
def get_my_report(db: Session = Depends(get_db)):
    return ReportRepository.get_medium_priority_report(db)


@router.get('/showLowPriorityReport', summary=None, name='SHOW_LOW_PRIORITY_REPORT', operation_id='get_low_priority_report')
def get_my_report(db: Session = Depends(get_db)):
    return ReportRepository.get_low_priority_report(db)


@router.put('/getSummary/{id}', summary=None, name='GET_SUMMARY', operation_id='get_summary')
def update_summary(id: str, db: Session = Depends(get_db)):
    return ReportRepository.update_summary(id, db)


@router.post('/create', summary=None, name='POST', operation_id='create_report', dependencies=[Depends(JWTBearer())])
def create(request: createReportModel, db: Session = Depends(get_db), id: UUID = Depends(JWTBearer())):
    return ReportRepository.create(request, db, JWTRepo.decode_token(id))


@router.put('/update/{id}', summary=None, name='UPDATE', operation_id='update_report')
def update(id: str, request: updateReportModel, db: Session = Depends(get_db)):
    return ReportRepository.update(id, request, db)


@router.put('/updateCategory/{id}', summary=None, name='UPDATE_CATEGORY', operation_id='update_report_category')
def update(id: str, request: updateCategoryModel, db: Session = Depends(get_db)):
    return ReportRepository.update_category(id, request, db)


@router.put('/updatePriority/{id}', summary=None, name='UPDATE_PRIORITY', operation_id='update_report_priority')
def update(id: str, request: updatePriorityModel, db: Session = Depends(get_db)):
    return ReportRepository.update_priority(id, request, db)


@router.put('/updateHeader/{id}', summary=None, name='UPDATE_HEADER', operation_id='update_report_header')
def update(id: str, request: updateHeaderModel, db: Session = Depends(get_db)):
    return ReportRepository.update_header(id, request, db)


@router.put('/updateInformation/{id}', summary=None, name='UPDATE_INFORMATION', operation_id='update_report_information')
def update(id: str, request: updateInformationModel, db: Session = Depends(get_db)):
    return ReportRepository.update_information(id, request, db)


@router.put('/markCompleted', summary=None, name='MARK_COMPLETED', operation_id='mark_completed_report')
def mark_completed(id: str, db: Session = Depends(get_db)):
    return ReportRepository.mark_completed(id, db)


@router.put('/unmarkCompleted', summary=None, name='UNMARK_COMPLETED', operation_id='unmark_completed_report')
def unmark_completed(id: str, db: Session = Depends(get_db)):
    return ReportRepository.unmark_completed(id, db)


@router.put('/markApproved', summary=None, name='MARK_APPROVED', operation_id='mark_approved_report')
def mark_approved(id: str, db: Session = Depends(get_db)):
    return ReportRepository.mark_aprroved(id, db)


@router.put('/unmarkApproved', summary=None, name='UNMARK_APPROVED', operation_id='unmark_approved_report')
def unmark_approved(id: str, db: Session = Depends(get_db)):
    return ReportRepository.unmark_aprroved(id, db)


@router.put('/markSpam', summary=None, name='MARK_SPAM', operation_id='mark_spam_report')
def mark_spam(id: str, db: Session = Depends(get_db)):
    return ReportRepository.mark_spam(id, db)


@router.put('/unmarkSpam', summary=None, name='UNMARK_SPAM', operation_id='unmark_spam_report')
def unmark_spam(id: str, db: Session = Depends(get_db)):
    return ReportRepository.unmark_spam(id, db)


@router.delete('/delete/{id}', summary=None, name='DELETE', operation_id='delete_report')
def remove(id: int, db: Session = Depends(get_db)):
    return ReportRepository.remove(id, db)
