import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import AccountModel
from .repository import AccountRepo

router = APIRouter(
    prefix="/Account",
    tags=['Accounts'],
    responses={422: {"description": "Validation Error"}},
)

@router.post('/create', summary=None, name='POST', operation_id='create')
def create(request: AccountModel, db: Session = Depends(get_db)):
    return AccountRepo.create(request, db)
