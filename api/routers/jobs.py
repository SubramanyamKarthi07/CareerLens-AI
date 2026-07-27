from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas import JobResponse
from api.services.analytics_service import (
    job_summary,
    job_search,
    job_filter,
    job_statistics
)

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.get(
    "",
    response_model=list[JobResponse]
)
def get_jobs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):

    offset = (page - 1) * limit

    return job_summary(
        db,
        limit=limit,
        offset=offset
    )

@router.get(
    "/search",
    response_model=list[JobResponse]
)
def search_job(
    keyword: str,
    db: Session = Depends(get_db)
):
    return job_search(db, keyword)

@router.get(
    "/filter",
    response_model=list[JobResponse]
)
@router.get(
    "/filter",
    response_model=list[JobResponse]
)
def filter_job(
    company: str | None = None,
    location: str | None = None,
    source: str | None = None,
    date_posted: str | None = None,
    sort_by: str = "date_posted",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    return job_filter(
        db,
        company,
        location,
        source,
        date_posted,
        sort_by,
        order
    )

@router.get("/statistics")
def get_job_statistics(
    db: Session = Depends(get_db)
):
    return job_statistics(db)