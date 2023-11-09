from core import BaseRepo
from sqlalchemy.orm import Session
from typing import Generic, TypeVar
from .entity import Account as AccountEntity
from .model import Account

T = TypeVar('T')

class AccountRepo(BaseRepo):
    def create(request: Account, db: Session):
        new_account = AccountEntity(username=request.username, email=request.email, password=request.password)
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account
