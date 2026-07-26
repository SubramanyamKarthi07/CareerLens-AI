from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas import SourceResponse
from api.services.analytics_service import source_summary

router = APIRouter(
    prefix="/sources",
    tags=["Sources"]
)


@router.get(
    "",
    response_model=list[SourceResponse]
)
def get_sources(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return source_summary(db)[:limit]