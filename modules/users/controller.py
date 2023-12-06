import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from .entity import UserEntity
from .repositorys import UserRepository
from .model import UserModel

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={422: {"description": "Validation Error"}},
)

@router.get(
    path="/all_user",
    dependencies=[Depends(JWTBearer())],
    summary="Get all users.",
    response_model=ResponseSchema,
    response_model_exclude_none=True,
    description="Get all users. Admin only."
)
async def get_user(db: Session = Depends(get_db), _token: str = Depends(JWTBearer())) -> ResponseSchema:
    try:
        _userId = JWTRepo.decode_token(_token.replace("Bearer ", ""))
        _user = UserRepository.get_by_id(db, UserEntity, _userId)
        if _user is None:
            raise HTTPException(status_code=404, detail="User not found.")
        if _user.role != 'Admin':
            raise HTTPException(status_code=403, detail="Forbidden.")

        _users = UserRepository.get_all(db, UserEntity)
        _list_user = [
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "profilePhoto": user.profilePhoto
            } for user in _users
        ]
        return ResponseSchema(
            code=200,
            status="S",
            result=_list_user
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.get(
        path="/user",
        dependencies=[Depends(JWTBearer())],
        response_model=ResponseSchema,
        response_model_exclude_none=True,
        summary="Get User Info by Token",
)
async def get_user_by_token(_token: str = Depends(JWTBearer()), db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        _user_id = JWTRepo.decode_token(_token.replace("Bearer ", ""))
        _user = UserRepository.get_by_id(db, UserEntity, _user_id)
        if _user is None:
            raise HTTPException(status_code=404, detail="User not found.")
        _user = {
            "id": str(_user.id),
            "username": _user.username,
            "email": _user.email,
            "role": _user.role,
            "profilePhoto": _user.profilePhoto
        }
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result=_user
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
