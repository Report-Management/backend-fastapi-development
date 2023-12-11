from core import BaseRepo
from sqlalchemy.orm import Session
from typing import TypeVar, Generic
from .model import UserEnum
from .entity import UserEntity

class UserRepository(BaseRepo):
    @staticmethod
    def update_role(id: str, db: Session, to_admin=False):
        user = db.query(UserEntity).filter(UserEntity.id == id).first()
        if user:
            if to_admin:
                user.role = UserEnum.Admin.value
                db.commit()
                db.refresh(user)
            else:
                user.role = UserEnum.Normal.value
                db.commit()
                db.refresh(user)

