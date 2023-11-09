import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .model import Account
from .entity import Account as AccountEntity
from .repositorys import UserRepo

router = APIRouter(
    prefix="/account",
    tags=['accounts']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Account, db: Session = Depends(get_db)):
    new_account = AccountEntity(username=request.username, email=request.email, password=request.password)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account
