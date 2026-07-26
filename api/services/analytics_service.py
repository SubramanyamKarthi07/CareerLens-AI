from api.crud import (
    get_dashboard_metrics,
    get_company_statistics,
    get_location_statistics,
    get_source_statistics,
    get_trend_statistics
)

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