from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas import TrendResponse
from api.services.analytics_service import trend_summary

router = APIRouter(
    prefix="/trends",
    tags=["Trends"]
)


@router.get(
    "",
    response_model=list[TrendResponse]
)
def get_trends(db: Session = Depends(get_db)):
    return trend_summary(db)