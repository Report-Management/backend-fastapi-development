from core import BaseRepo
from sqlalchemy.orm import Session
from typing import Generic, TypeVar

T = TypeVar('T')

class UserRepo(BaseRepo):
    @staticmethod
    def find_by_username(db: Session, model: Generic[T], username: str):
        return db.query(model).filter(model.username == username).first()
