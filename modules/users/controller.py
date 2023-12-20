import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from core import get_db, ResponseSchema, JWTBearer, JWTRepo, StatusEnum, SupabaseService
from .entity import UserEntity
from .repositorys import UserRepository
from .model import UserModel, UserEnum
import resend
from helper import sent_email
from supabase import PostgrestAPIError

router = APIRouter(
    prefix="/user",
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
        if _user.role != UserEnum.Admin.value:
            raise HTTPException(status_code=403, detail="Forbidden.")
        _users = UserRepository.get_all(db, UserEntity)
        _list_user = []
        for user in _users:
            if str(user.id) != _userId:
                _list_user.append(
                    {
                        "id": str(user.id),
                        "username": user.username,
                        "email": user.email,
                        "role": user.role,
                        "profilePhoto": user.profilePhoto
                    }
                )

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
        path="/get_me",
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

@router.put(
    path='/to_admin/{id}',
    name="Upgrade user role to admin",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseSchema,
    response_model_exclude_none=True,
    summary="Get User Info by Token",
)
def update(id: str, db: Session = Depends(get_db), _token: str = Depends(JWTBearer())):
    if id is not type(str):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    try:
        _userId = JWTRepo.decode_token(_token.replace("Bearer ", ""))
        _user = UserRepository.get_by_id(db, UserEntity, _userId)
        if _user is None:
            raise HTTPException(status_code=404, detail="User not found.")
        if _user.role != 'Admin':
            raise HTTPException(status_code=403, detail="Forbidden.")
        UserRepository.update_role(id=id, db=db, to_admin=True)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update to admin successfully"
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.put(
    path='/to_normal/{id}',
    name="Upgrade user role to normal",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseSchema,
    response_model_exclude_none=True,
    summary="Get User Info by Token",
)
def update(id: str, db: Session = Depends(get_db), _token: str = Depends(JWTBearer())):
    try:
        _userId = JWTRepo.decode_token(_token.replace("Bearer ", ""))
        _user = UserRepository.get_by_id(db, UserEntity, _userId)

        if not isinstance(id, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad Request"
            )

        if _user is None or _user.role != 'Admin':
            raise HTTPException(status_code=403, detail="Forbidden.")

        UserRepository.update_role(id=id, db=db, to_admin=False)
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status=StatusEnum.Success.value,
            message="Update to normal successfully"
        )
    except HTTPException as http_error:
        raise http_error
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.delete(
    path="/delete_user/{id}",
    summary="Delete User",
    dependencies=[Depends(JWTBearer())],
    response_model=ResponseSchema,
    response_model_exclude_none=True,
    description="Admin can delete user account."
)
def delete_user(id: str, db: Session = Depends(get_db), _token: str = Depends(JWTBearer())):
    try:
        _userId = JWTRepo.decode_token(_token)
        _userId = uuid.UUID(_userId)
        _user = UserRepository.get_by_id(db, UserEntity, _userId)

        if not _user or _user.role != 'Admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

        d_user = UserRepository.get_by_id(db, UserEntity, id)
        if not d_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        is_deleted_auth = SupabaseService.delete_user(id)
        if is_deleted_auth:
            is_deleted = UserRepository.delete_by_id(db, UserEntity, d_user.id)
            if is_deleted:
                return ResponseSchema(
                    code=status.HTTP_200_OK,
                    status="S",
                    message="Delete Completed"
                )
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Not found user_id")
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
