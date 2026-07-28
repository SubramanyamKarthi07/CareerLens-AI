from api.repositories.analytics_repository import (
    get_dashboard_metrics,
    get_company_statistics,
    get_location_statistics,
    get_source_statistics,
    get_trend_statistics,
    get_job_list,
    search_jobs,
    filter_jobs,
    get_job_statistics,
)

from api.crud import recommend_jobs

def dashboard_summary(db):
    return get_dashboard_metrics(db)


def company_summary(db):
    return get_company_statistics(db)


def location_summary(db):
    return get_location_statistics(db)

def source_summary(db):
    return get_source_statistics(db)

def trend_summary(db):
    return get_trend_statistics(db)

def job_summary(db, limit=20, offset=0):
    return get_job_list(db, limit, offset)

def job_search(db, keyword):
    return search_jobs(db, keyword)

def job_filter(
    db,
    company=None,
    location=None,
    source=None,
    date_posted=None,
    sort_by="date_posted",
    order="desc"
):
    return filter_jobs(
        db,
        company,
        location,
        source,
        date_posted,
        sort_by,
        order
    )

def job_statistics(db):
    return get_job_statistics(db)

def job_recommendation(db, skills):
    return recommend_jobs(db, skills)