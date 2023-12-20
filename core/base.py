from jose import jwt
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta, datetime
from fastapi import Request, HTTPException, Depends, status
from typing import TypeVar, Generic, Optional, Dict
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .database import SECRET_KEY, ALGORITHM

T = TypeVar('T')

class BaseRepo:

    @staticmethod
    def get_all(db: Session, model=Generic[T]):
        return db.query(model).all()

    @staticmethod
    def get_by_id(db: Session, model: Generic[T], id: UUID):
        return db.query(model).filter(model.id == id).first()

    @staticmethod
    def insert(db: Session, model: Generic[T]):
        try:
            db.add(model)
            db.commit()
            return model
        except SQLAlchemyError as e:
            print(f"Insertion failed: {e}")
            db.rollback()
            return None

    @staticmethod
    def update(db: Session, model: Generic[T]):
        try:
            db.commit()
            db.refresh(model)
            return model
        except SQLAlchemyError as e:
            print(f"Update failed: {e}")
            db.rollback()
            return None

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        try:
            db.delete(model)
            db.commit()
        except SQLAlchemyError as e:
            print(f"Deletion failed: {e}")
            db.rollback()
            return False

    @staticmethod
    def delete_by_id(db: Session, model: Generic[T], id: UUID):
        instance = db.query(model).get(id)
        if instance:
            db.delete(instance)
            db.commit()
            return True
        return False


class JWTRepo:
    @staticmethod
    def generate_token(data: dict):
        to_encode = data.copy()
        to_encode["aud"] = "authenticated"
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="authenticated")
            return payload.get('sub')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.")
        except jwt.JWTError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden.")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    def get_token(request: Request):
        credentials: HTTPAuthorizationCredentials = JWTBearer()(request)
        return credentials.credentials


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication schema.")
            if self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwt_token: str):
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithm=[ALGORITHM], audience="authenticated")
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid