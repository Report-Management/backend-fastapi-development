from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .repository import DashboardRepository
from core import get_db

router = APIRouter(
    prefix="/dashboard",
    tags=['Dashboard'],
    responses={422: {"description": "Validation Error"}},
)


@router.get("/month", operation_id='dashboard_month')
def dashboard_month(year, db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_month(db, year)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/year",  operation_id='dashboard_year')
def dashboard_year(db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_year(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/detail", operation_id='dashboard_detail')
def dashboard_detail(db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_detail(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/category/all", operation_id='dashboard_categoty_all')
def dashboard_category_all(db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_category_all(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/category", operation_id='dashboard_category_year')
def dashboard_category_year(year, db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_category_year(db, year)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/solve", operation_id='dashboard_solve')
def dashboard_solve(year, month, db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_solve(db, year, month)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/spam", operation_id='dashboard_spam')
def dashboard_spam(year, month, db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_spam(db, year, month)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")


@router.get("/date", operation_id='dashboard_date')
def dashboard_date(db: Session = Depends(get_db)):
    try:
        return DashboardRepository.dashboard_date(db)
    except HTTPException as http_error:
        raise http_error
    except Exception:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
