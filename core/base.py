import jwt
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from fastapi import Request, HTTPException
from typing import TypeVar, Generic, Optional
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
        db.add(model)
        db.commit()
        db.refresh(model)

    @staticmethod
    def update(db: Session, model: Generic[T]):
        db.commit()
        db.refresh(model)

    @staticmethod
    def delete(db: Session, model: Generic[T]):
        db.delete(model)
        db.commit()


class JWTRepo:

    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encode_jwt

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("id")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="Token expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token.")
        except Exception as e:
            return {}

    @staticmethod
    def get_token(request: Request):
        credentials: HTTPAuthorizationCredentials = JWTBearer()(request)
        return credentials.credentials


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        JWTBearer.__name__ = "Bearer"
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
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithm=[ALGORITHM])
        except:
            payload = None

        if payload:
            isTokenValid = True
        return isTokenValid
