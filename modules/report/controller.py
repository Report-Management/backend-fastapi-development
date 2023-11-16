import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import ReportModel
from .repository import ReportRepository

router = APIRouter(
    prefix="/Report",
    tags=['Reports'],
    responses={422: {"description": "Validation Error"}},
)

@router.post('/create', summary=None, name='POST', operation_id='create')
def create(request: ReportModel, db: Session = Depends(get_db)):
    return ReportRepository.create(request, db)

@router.delete('/delete/{id}', summary=None, name='DELETE', operation_id='delete')
def remove(id: int, request: ReportModel, db: Session = Depends(get_db)):
    return ReportRepository.remove(id, request, db)
