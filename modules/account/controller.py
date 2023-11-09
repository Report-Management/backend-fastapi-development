import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import Account
from .repository import AccountRepo

router = APIRouter(
    prefix="/account",
    tags=['accounts']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Account, db: Session = Depends(get_db)):
    return AccountRepo.create(request, db)
