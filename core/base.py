import jwt
from sqlalchemy import UUID
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from fastapi import Request, HTTPException, Depends
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
            raise HTTPException(status_code=403, detail="Token expired.")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Forbidden.")
        except Exception as e:
            return {}

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


class AdminDepends:
    def __init__(self):
        self.check_admin()

    @staticmethod
    def check_admin(_token: str = Depends(JWTBearer())):
        _user_id = JWTRepo.decode_token(_token.replace("Bearer ", ""))
        _user_id = uuid.UUID(_user_id)
        _user = UserRepository.get_by_id(db, UserEntity, _user_id)

        if _user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if _user.role != 'Admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return _user

