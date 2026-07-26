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

def get_location_statistics(db):

    query = text("""
        SELECT
            l.location_id,
            l.location_name,
            COUNT(j.job_id) AS total_jobs
        FROM locations l
        JOIN job_postings j
            ON l.location_id = j.location_id
        GROUP BY
            l.location_id,
            l.location_name
        ORDER BY total_jobs DESC;
    """)

    result = db.execute(query)

    locations = []

    for row in result:
        locations.append({
            "location_id": row.location_id,
            "location_name": row.location_name,
            "total_jobs": row.total_jobs
        })

    return locations


def get_source_statistics(db):

    query = text("""
        SELECT
            s.source_id,
            s.source_name,
            COUNT(j.job_id) AS total_jobs
        FROM sources s
        JOIN job_postings j
            ON s.source_id = j.source_id
        GROUP BY
            s.source_id,
            s.source_name
        ORDER BY total_jobs DESC;
    """)

    result = db.execute(query)

    sources = []

    for row in result:
        sources.append({
            "source_id": row.source_id,
            "source_name": row.source_name,
            "total_jobs": row.total_jobs
        })

    return sources


def get_trend_statistics(db):

    query = text("""
        SELECT
            date_posted,
            COUNT(*) AS total_jobs
        FROM job_postings
        GROUP BY date_posted
        ORDER BY date_posted;
    """)

    result = db.execute(query)

    trends = []

    for row in result:
        trends.append({
            "date_posted": str(row.date_posted),
            "total_jobs": row.total_jobs
        })

    return trends