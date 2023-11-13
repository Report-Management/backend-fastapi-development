import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from core import get_db, ResponseSchema, JWTBearer, JWTRepo
from fastapi.exceptions import RequestValidationError
from .model import AccountModel
from .repository import AccountRepo
from .entity import AccountEntity
from core.supabase import SupabaseService
router = APIRouter(
    prefix="/Account",
    tags=['Accounts'],
    responses={422: {"description": "Validation Error"}},
    
)

@router.post('/create', summary=None, name='POST', operation_id='create', status_code=status.HTTP_200_OK)
def create(request: AccountModel, db: Session = Depends(get_db)):
    try:
        res = SupabaseService().supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "username": request.username,
                    "email": request.email,
                    "role": request.role,
                }
            }
        })
        print(res.user.id)
        _account = AccountEntity(
            accountID=uuid.UUID(res.user.id),
            username=request.username,
            email=request.email,
            password=request.password,
            role=request.role,
        )
        AccountRepo.insert(db, _account)
        return HTTPException(status_code=200, detail="Account created.")
    except Exception as error:
        print(error.args)
        return HTTPException(status_code=500, detail="Failed to create account.")

