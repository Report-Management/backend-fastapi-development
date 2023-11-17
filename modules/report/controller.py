import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import ReportModel
from .repository import ReportRepository
from sqlalchemy import UUID

router = APIRouter(
    prefix="/Report",
    tags=['Reports'],
    responses={422: {"description": "Validation Error"}},
)

@router.post('/create', summary=None, name='POST', operation_id='create_report', dependencies=[Depends(JWTBearer())])
def create(request: ReportModel, db: Session = Depends(get_db), id: UUID = Depends(JWTBearer())):
    print(JWTRepo.decode_token(id))
    return ReportRepository.create(request, db, JWTRepo.decode_token(id))

@router.delete('/delete/{id}', summary=None, name='DELETE', operation_id='delete')
def remove(id: int, request: ReportModel, db: Session = Depends(get_db)):
    return ReportRepository.remove(id, request, db)
