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

def get_job_list(db, limit=20, offset=0):

    query = text("""
        SELECT
            j.job_id,
            j.title,
            c.company_name AS company,
            l.location_name AS location,
            s.source_name AS source,
            j.date_posted,
            j.description,
            j.link
        FROM job_postings j

        JOIN companies c
            ON j.company_id = c.company_id

        JOIN locations l
            ON j.location_id = l.location_id

        JOIN sources s
            ON j.source_id = s.source_id

        ORDER BY j.job_id
        LIMIT :limit
        OFFSET :offset;
    """)

    result = db.execute(
        query,
        {
            "limit": limit,
            "offset": offset
        }
    )

    jobs = []

    for row in result:
        jobs.append({
            "job_id": row.job_id,
            "title": row.title,
            "company": row.company,
            "location": row.location,
            "source": row.source,
            "date_posted": str(row.date_posted),
            "description": row.description,
            "link": row.link
        })

    return jobs


def search_jobs(db, keyword: str):

    query = text("""
        SELECT
            j.job_id,
            j.title,
            c.company_name,
            l.location_name,
            s.source_name,
            j.date_posted,
            j.description,
            j.link
        FROM job_postings j
        JOIN companies c
            ON j.company_id = c.company_id
        JOIN locations l
            ON j.location_id = l.location_id
        JOIN sources s
            ON j.source_id = s.source_id
        WHERE
            LOWER(j.title) LIKE LOWER(:keyword)
            OR LOWER(j.description) LIKE LOWER(:keyword)
        ORDER BY j.date_posted DESC;
    """)

    result = db.execute(
        query,
        {"keyword": f"%{keyword}%"}
    )

    jobs = []

    for row in result:
        jobs.append({
            "job_id": row.job_id,
            "title": row.title,
            "company": row.company_name,
            "location": row.location_name,
            "source": row.source_name,
            "date_posted": str(row.date_posted),
            "description": row.description,
            "link": row.link
        })

    return jobs


def filter_jobs(
    db,
    company=None,
    location=None,
    source=None,
    date_posted=None,
    sort_by="date_posted",
    order="desc"
):

    query = """
        SELECT
            j.job_id,
            j.title,
            c.company_name AS company,
            l.location_name AS location,
            s.source_name AS source,
            j.date_posted,
            j.description,
            j.link
        FROM job_postings j

        JOIN companies c
            ON j.company_id = c.company_id

        JOIN locations l
            ON j.location_id = l.location_id

        JOIN sources s
            ON j.source_id = s.source_id
    """

    conditions = []
    params = {}

    if company:
        conditions.append(
            "LOWER(c.company_name) LIKE LOWER(:company)"
        )
        params["company"] = f"%{company}%"

    if location:
        conditions.append(
            "LOWER(l.location_name) LIKE LOWER(:location)"
        )
        params["location"] = f"%{location}%"

    if source:
        conditions.append(
            "LOWER(s.source_name) LIKE LOWER(:source)"
        )
        params["source"] = f"%{source}%"

    if date_posted:
        conditions.append(
            "j.date_posted = :date_posted"
        )
        params["date_posted"] = date_posted

    if conditions:
        query += "\nWHERE " + "\nAND ".join(conditions)

    # Allowed sorting columns
    sort_columns = {
        "date_posted": "j.date_posted",
        "title": "j.title",
        "company": "c.company_name",
        "location": "l.location_name",
        "source": "s.source_name"
    }

    # Get the database column for sorting
    sort_column = sort_columns.get(sort_by, "j.date_posted")

    # Determine sorting order
    sort_order = "ASC" if order.lower() == "asc" else "DESC"

    query += f"""
        ORDER BY {sort_column} {sort_order};
    """

    result = db.execute(
        text(query),
        params
    )

    jobs = []

    for row in result:
        jobs.append({
            "job_id": row.job_id,
            "title": row.title,
            "company": row.company,
            "location": row.location,
            "source": row.source,
            "date_posted": str(row.date_posted),
            "description": row.description,
            "link": row.link
        })

    return jobs


def get_job_statistics(db):

    query = text("""
        SELECT
            COUNT(*) AS total_jobs,
            COUNT(DISTINCT company_id) AS unique_companies,
            COUNT(DISTINCT location_id) AS unique_locations,
            COUNT(DISTINCT source_id) AS unique_sources,
            MIN(date_posted) AS oldest_job_date,
            MAX(date_posted) AS latest_job_date
        FROM job_postings;
    """)

    result = db.execute(query).fetchone()

    return {
        "total_jobs": result.total_jobs,
        "unique_companies": result.unique_companies,
        "unique_locations": result.unique_locations,
        "unique_sources": result.unique_sources,
        "oldest_job_date": str(result.oldest_job_date),
        "latest_job_date": str(result.latest_job_date)
    }