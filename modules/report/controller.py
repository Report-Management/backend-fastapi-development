import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import Report
from .repository import ReportRepo

router = APIRouter(
    prefix="/report",
    tags=['reports']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Report, db: Session = Depends(get_db)):
    return ReportRepo.create(request, db)
