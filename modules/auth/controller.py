from passlib.context import CryptContext
from sqlalchemy.orm import Session
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from core import get_db, JWTRepo, TokenResponse, ResponseSchema, JWTBearer, SupabaseService
from modules.users import UserModel, UserLoginModel, UserEntity, UserRepository
from .repository import AuthRepository
from .model import AccountType

router = APIRouter(
    prefix="/authentications",
    tags=["Authentications"],
    responses={422: {"description": "Validation Error"}},
)

@router.post(
    path='/login',
    summary="Login",
    response_model=ResponseSchema,
    response_model_exclude_none=True,
    description="Login to get access token."
)
def login(request: UserLoginModel, db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        _user = AuthRepository.find_by_email(db, UserEntity, request.email)
        if _user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if not pwd_context.verify(request.password, _user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

        _token = JWTRepo.generate_token({"sub": str(_user.id)})

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                "access_token": _token,
                "type": "bearer"
            }
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")

@router.post(
        path='/create',
        summary="Create User",
        dependencies=[Depends(JWTBearer())],
        response_model=ResponseSchema,
        response_model_exclude_none=True,
        description="Admin create user account."
)
def create(body: UserModel, db: Session = Depends(get_db), _token: str = Depends(JWTBearer())):
    try:
        _userId = JWTRepo.decode_token(_token)
        _userId = uuid.UUID(_userId)
        _user = UserRepository.get_by_id(db, UserEntity, _userId)

        if _user is None:
            raise HTTPException(status_code=404, detail="Email not found")
        if _user.role != 'Admin':
            raise HTTPException(status_code=403, detail="Forbidden")
        if (body.role is None) or (body.role == "") or (body.role not in [role.value for role in AccountType]):
            raise HTTPException(status_code=422, detail="Invalid role")

        res = SupabaseService().supabase.auth.sign_up({
            "email": body.email,
            "password": body.password,
            "options": {
                "data": {
                    "username": body.username,
                    "email": body.email,
                }
            }
        })

        sent_email(
            sender="admin@reportmanagement.online",
            to=body.email,
            body={
                "username": body.username,
                "email": body.email,
                "password": body.password
            }
        )

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        _account = UserEntity(
            id=uuid.UUID(res.user.id),
            username=body.username,
            email=body.email,
            password=pwd_context.hash(body.password),
            role=body.role,
        )
        is_inserted = UserRepository.insert(db, _account)
        if is_inserted is None:
            raise HTTPException(status_code=500, detail="Internal server error.")
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            message="User created successfully."
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(error.args)
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get(
    path='/check/{id}',
    summary="Check Role",
    name='GET',
    response_model=ResponseSchema,
    response_model_exclude_none=True,
    description="Check user role. Admin or User."
)
async def check(id: str, db: Session = Depends(get_db)) -> ResponseSchema:
    try:
        _user = UserRepository.get_by_id(db, UserEntity, id)
        if _user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                "role": _user.role
            }
        )
    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal server error.")
