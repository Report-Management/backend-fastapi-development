from core import BaseRepo
from sqlalchemy.orm import Session
from .entity import AccountEntity
from .model import AccountModel

class AccountRepo(BaseRepo):
    
    @staticmethod
    def create(request: AccountModel, db: Session):
        new_account = AccountEntity(username=request.username, email=request.email, password=request.password)
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account
