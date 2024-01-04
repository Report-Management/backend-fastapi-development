import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, UploadFile, File, Form, HTTPException
from core import get_db, ResponseSchema, JWTBearer, JWTRepo, SupabaseService, StatusEnum
from .model import *
from .repository import ReportRepository
from sqlalchemy import UUID, extract
from datetime import datetime, timedelta
from typing import TypeVar, Annotated, Dict


router = APIRouter(
    prefix="/report",
    tags=['Reports'],
    responses={422: {"description": "Validation Error"}},
)

@router.get(path='/show', summary="Get all report", response_model=ResponseSchema, response_model_exclude_none=True, description="Fetch all report and filter")
def get_all_reports(
        types: TypeEnum = None,
        priority: PriorityEnum = None,
        category: CategoryEnum = None,
        date: DateEnum = None,
        db: Session = Depends(get_db),
):
    filters: Dict[FilterEnum, Enum] = {}
    if types:
        filters[FilterEnum.Type] = types
    if priority:
        filters[FilterEnum.Priority] = priority
    if category:
        filters[FilterEnum.Category] = category
    if date:
        filters[FilterEnum.Date] = date
    try:
        return ReportRepository.get_all_reports(db, filters)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get(path='/show/approve', summary="Get report that approve", response_model=ResponseSchema, response_model_exclude_none=True, description="Fetch all report that approve")
def get_approve_reports(db: Session = Depends(get_db)):
    try:
        return ReportRepository.get_all_approve_reports(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.get(path='/show/{id}', name='Show by id', response_model=ResponseSchema, response_model_exclude_none=True,)
def get_report(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.get_report(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.get(path='/showMyReport', name='SHOW MY REPORT', response_model=ResponseSchema, response_model_exclude_none=True)
def get_my_report(token: UUID = Depends(JWTBearer()), db: Session = Depends(get_db)):
    try:
        return ReportRepository.get_my_report(JWTRepo.decode_token(token), db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get(path='/showCompletedReport', name="Show completed report", response_model=ResponseSchema, response_model_exclude_none=True)
def get_my_report(db: Session = Depends(get_db)):
    try:
        return ReportRepository.get_completed_report(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get(path='/showSpamReport', name='SHOW_SPAM_REPORT', response_model=ResponseSchema, response_model_exclude_none=True)
def get_spam_report(db: Session = Depends(get_db)):
    try:
        return ReportRepository.get_spam_report(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.get(path='/search', name='SEARCH_REPORT', response_model=ResponseSchema, response_model_exclude_none=True)
def search_report(search: str, db: Session = Depends(get_db)):
    try:
        return ReportRepository.search_report(search, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.post(path='/create', name='POST', dependencies=[Depends(JWTBearer())], response_model=ResponseSchema,
             response_model_exclude_none=True)
def create(
        category: Annotated[CategoryEnum, Form()],
        priority: Annotated[PriorityEnum, Form()],
        header: Annotated[str, Form()],
        information: Annotated[str, Form()],
        view: Annotated[ViewEnum, Form()],
        file: UploadFile = File(None),
        db: Session = Depends(get_db),
        token: UUID = Depends(JWTBearer())
):
    report_id = uuid.uuid4()
    if file:
        bucket = 'testbucket'
        file = SupabaseService.upload_file(bucket, file, str(report_id))

    body = CreateReportModel(
        id=report_id,
        category=category.value,
        priority=priority.value,
        header=header,
        information=information,
        view=view.value,
        file=file,
    )
    try:
        return ReportRepository.create(body, db, JWTRepo.decode_token(token))
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.get('/getSummary/{id}', name='GET_SUMMARY', response_model=ResponseSchema, response_model_exclude_none=True)
def update_summary(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.update_summary(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put('/update/{id}', name='UPDATE', response_model=ResponseSchema, response_model_exclude_none=True)
def update(id: str, request: UpdateReportModel, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.update_report(id, request, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.put('/updateCategory/{id}', name='UPDATE_CATEGORY', response_model=ResponseSchema, response_model_exclude_none=True)
def update(id: str, category: CategoryEnum, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.update_category(id, category, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.put('/updatePriority/{id}', name='UPDATE_PRIORITY', response_model=ResponseSchema, response_model_exclude_none=True)
def update(id: str, priority: PriorityEnum, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    return ReportRepository.update_priority(id, priority, db)


@router.put('/updateHeader/{id}', name='UPDATE_HEADER', response_model=ResponseSchema, response_model_exclude_none=True)
def update(id: str, header: UpdateHeaderModel, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.update_header(id, header, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put('/updateInformation/{id}', name='UPDATE_INFORMATION', response_model=ResponseSchema, response_model_exclude_none=True)
def update(id: str, infor: UpdateInformationModel, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.update_information(id, infor, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put('/markCompleted', name='MARK_COMPLETED', response_model=ResponseSchema, response_model_exclude_none=True)
def mark_completed(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.mark_completed(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.put('/unmarkCompleted', name='UNMARK_COMPLETED', response_model=ResponseSchema, response_model_exclude_none=True)
def unmark_completed(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.unmark_completed(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put('/markApproved', name='MARK_APPROVED', response_model=ResponseSchema, response_model_exclude_none=True)
def mark_approved(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.mark_approved(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put('/unmarkApproved', name='UNMARK_APPROVED', response_model=ResponseSchema, response_model_exclude_none=True)
def unmark_approved(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.unmark_approved(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put('/markSpam', name='MARK_SPAM', response_model=ResponseSchema, response_model_exclude_none=True)
def mark_spam(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.mark_spam(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.put('/unmarkSpam', name='UNMARK_SPAM', response_model=ResponseSchema, response_model_exclude_none=True)
def unmark_spam(id: str, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.unmark_spam(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put(path='/updateFile/{id}', name="UPDATE_FILE", response_model=ResponseSchema, response_model_exclude_none=True)
def upload_file(id: str, file: UploadFile, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.update_file(id, file, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.delete(path='/uploadFile/{id}', name="REMOVE_FILE", response_model=ResponseSchema, response_model_exclude_none=True)
def remove_file(id: str,  db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.remove_file(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.delete('/delete/{id}', name='DELETE', operation_id='delete_report')
def remove(id: int, db: Session = Depends(get_db)):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        return ReportRepository.remove(id, db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
