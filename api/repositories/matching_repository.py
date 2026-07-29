from sqlalchemy.orm import Session
from sqlalchemy import text


def get_all_jobs(db: Session):
    query = text("""
        SELECT
            jp.job_id,
            jp.title,
            jp.description,
            jp.link,
            c.company_name,
            l.location_name,
            s.source_name
        FROM job_postings jp
        LEFT JOIN companies c
            ON jp.company_id = c.company_id
        LEFT JOIN locations l
            ON jp.location_id = l.location_id
        LEFT JOIN sources s
            ON jp.source_id = s.source_id
    """)

    result = db.execute(query)

    return result.mappings().all()