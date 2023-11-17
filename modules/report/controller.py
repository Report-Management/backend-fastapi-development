import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import createReportModel, updateReportModel
from .repository import ReportRepository
from sqlalchemy import UUID

router = APIRouter(
    prefix="/Report",
    tags=['Reports'],
    responses={422: {"description": "Validation Error"}},
)


@router.post('/create', summary=None, name='POST', operation_id='create_report', dependencies=[Depends(JWTBearer())])
def create(request: createReportModel, db: Session = Depends(get_db), id: UUID = Depends(JWTBearer())):
    return ReportRepository.create(request, db, JWTRepo.decode_token(id))


@router.put('/update/{id}', summary=None, name='UPDATE', operation_id='update_report')
def update(request: updateReportModel, db: Session = Depends(get_db)):
    return ReportRepository.update(id, request, db)


@router.delete('/delete/{id}', summary=None, name='DELETE', operation_id='delete_report')
def remove(id: int, db: Session = Depends(get_db)):
    return ReportRepository.remove(id, db)
