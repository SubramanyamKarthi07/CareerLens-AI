from sqlalchemy import text

def recommend_jobs(db, skills: list[str]):

    query = text("""
        SELECT
            j.job_id,
            j.title,
            c.company_name AS company,
            l.location_name AS location,
            s.source_name AS source,
            j.description
        FROM job_postings j

        JOIN companies c
            ON j.company_id = c.company_id

        JOIN locations l
            ON j.location_id = l.location_id

        JOIN sources s
            ON j.source_id = s.source_id;
    """)

    result = db.execute(query)

    recommendations = []

    # Convert user skills to lowercase
    user_skills = [skill.lower() for skill in skills]

    for row in result:

        description = (row.description or "").lower()

        matched_skills = [
            skill for skill in user_skills
            if skill in description
        ]

        match_score = (
            len(matched_skills) / len(user_skills)
        ) * 100

        if match_score > 0:
            recommendations.append({
                "job_id": row.job_id,
                "title": row.title,
                "company": row.company,
                "location": row.location,
                "source": row.source,
                "match_score": round(match_score, 2)
            })

    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    return recommendations[:10]