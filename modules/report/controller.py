import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import Report
from .entity import Report as ReportEntity
from .repositorys import UserRepo

router = APIRouter(
    prefix="/report",
    tags=['reports']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Report, db: Session = Depends(get_db)):
    new_report = ReportEntity(category=request.category, priority=request.priority, header=request.header, information=request.information, view=request.view, spam=request.spam, accountID=1)
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
