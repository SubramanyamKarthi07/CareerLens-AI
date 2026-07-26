from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas import LocationResponse
from api.services.analytics_service import location_summary

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.get(
    "",
    response_model=list[LocationResponse]
)
def get_locations(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return location_summary(db)[:limit]