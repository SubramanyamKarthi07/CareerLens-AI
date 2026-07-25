from api.crud import (
    get_dashboard_metrics,
    get_company_statistics
)


def dashboard_summary(db):
    return get_dashboard_metrics(db)


def company_summary(db):
    return get_company_statistics(db)