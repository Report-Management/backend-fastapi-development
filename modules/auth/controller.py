from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from core import get_db, JWTRepo, TokenResponse, ResponseSchema, JWTBearer, SupabaseService
from modules.users import UserModel, UserLoginModel, UserEntity, UserRepository
from .repository import AuthRepository

router = APIRouter(
    prefix="/Authentications",
    tags=["Authentications"],
    responses={422: {"description": "Validation Error"}},
)

@router.post('/login', summary=None, name='POST', operation_id='login', response_model=ResponseSchema)
def login(request: UserLoginModel, db: Session = Depends(get_db)):
    try:
        _user = AuthRepository.find_by_email(db, UserEntity, request.email)

        if _user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        if not pwd_context.verify(request.password, _user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

        _token = JWTRepo.generate_token({"id": str(_user.id)})

        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                "token": _token,
                "token_type": "bearer"
            }
        )


    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to login.")

@router.post('/create', summary=None, name='POST', operation_id='create', dependencies=[Depends(JWTBearer())])
def create(request: UserModel, db: Session = Depends(get_db), _token: str = Depends(JWTBearer())):
    try:
        _userId = JWTRepo.decode_token(_token)
        _user = UserRepository.get_by_id(db, UserEntity, _userId)
        print(_user.role)
        if _user is None:
            return HTTPException(status_code=404, detail="Email not found")
        if _user.role != 'Admin':
            return HTTPException(status_code=403, detail="Forbidden")

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
        return ResponseSchema(
            code=status.HTTP_200_OK,
            status="S",
            result={
                "message": "Account created successfully."
            }
        )

    except HTTPException as http_error:
        raise http_error
    except Exception as error:
        print(error.args)
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get('/check', summary=None, name='GET', operation_id='check_role')
async def check(id: str, db: Session = Depends(get_db)):
    try:
        _user = UserRepository.get_by_id(db, UserEntity, id)
        print(_user.role)
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
        raise HTTPException(status_code=500, detail="Internal server error.")


