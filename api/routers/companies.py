from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas import CompanyResponse
from api.services.analytics_service import company_summary

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


@router.get(
    "",
    response_model=list[CompanyResponse]
)
def get_companies(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return company_summary(db)[:limit]