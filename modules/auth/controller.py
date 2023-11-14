from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from core import get_db, JWTRepo, TokenResponse, ResponseSchema, JWTBearer, SupabaseService
from modules.users import UserModel, UserRepository, UserLoginModel, UserEntity
import uuid

router = APIRouter(
    prefix="/Authentications",
    tags=["Authentications"],
    responses={422: {"description": "Validation Error"}},
)

@router.post('/create', summary=None, name='POST', operation_id='create', dependencies=[Depends(JWTBearer())])
def create(request: UserModel, db: Session = Depends(get_db), _token: str = Depends(JWTBearer())):
    _userId = JWTRepo.decode_token(_token)
    _user = UserRepository.get_by_id(db, UserEntity, _userId)
    print(_user.role)
    if _user is None:
        return HTTPException(status_code=404, detail="User not found")
    if _user.role != 'Admin':
        return HTTPException(status_code=403, detail="Forbidden")
    try:
        res = SupabaseService().supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "username": request.username,
                    "email": request.email,
                }
            }
        })
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        _account = UserEntity(
            id=uuid.UUID(res.user.id),
            username=request.username,
            email=request.email,
            password=pwd_context.hash(request.password),
            role=request.role,
        )
        UserRepository.insert(db, _account)
        return HTTPException(status_code=200, detail="Account created.")
    except RequestValidationError as error:
        print(error.errors())
        raise HTTPException(status_code=422, detail="Validation Error.")
    except TimeoutError as error:
        SupabaseService().supabase.auth.admin.delete_user(res.user.id)
        raise HTTPException(status_code=408, detail="Request Timeout.")
    except Exception as error:
        print(error.args)
        raise HTTPException(status_code=500, detail="Failed to create account.")

@router.get('/check', summary=None, name='GET', operation_id='check_role')
async def check(id: str, db: Session = Depends(get_db)):
    try:
        _user = UserRepository.get_by_id(db, UserEntity, id)
        print(_user.role)
        if _user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return HTTPException(status_code=200, detail=_user.role)
    except Exception as error:
        raise HTTPException(status_code=500, detail="Failed to check role.")
