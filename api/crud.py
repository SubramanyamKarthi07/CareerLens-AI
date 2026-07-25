from sqlalchemy import text


def get_dashboard_metrics(db):

    total_jobs = db.execute(
        text("SELECT COUNT(*) FROM job_postings")
    ).scalar()

    total_companies = db.execute(
        text("SELECT COUNT(*) FROM companies")
    ).scalar()

    total_locations = db.execute(
        text("SELECT COUNT(*) FROM locations")
    ).scalar()

    total_sources = db.execute(
        text("SELECT COUNT(*) FROM sources")
    ).scalar()

    return {
        "total_jobs": total_jobs,
        "total_companies": total_companies,
        "total_locations": total_locations,
        "total_sources": total_sources,
    }

def get_company_statistics(db):

    query = text("""
        SELECT
            c.company_id,
            c.company_name,
            COUNT(j.job_id) AS total_jobs
        FROM companies c
        JOIN job_postings j
            ON c.company_id = j.company_id
        GROUP BY
            c.company_id,
            c.company_name
        ORDER BY total_jobs DESC;
    """)

    result = db.execute(query)

    companies = []

    for row in result:
        companies.append({
            "company_id": row.company_id,
            "company_name": row.company_name,
            "total_jobs": row.total_jobs
        })

    return companies