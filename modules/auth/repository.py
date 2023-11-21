from core import BaseRepo
from sqlalchemy.orm import Session
from typing import TypeVar, Generic

T = TypeVar('T')

class AuthRepository(BaseRepo):

    @staticmethod
    def find_by_email(db: Session, model: Generic[T], email: str):
        return db.query(model).filter(model.email == email).first()