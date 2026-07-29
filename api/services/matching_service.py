from sqlalchemy.orm import Session

from api.services.skill_service import get_resume_skills
from api.repositories.matching_repository import get_all_jobs
from api.repositories.skill_repository import extract_skills


def match_resume_with_jobs(db: Session, resume_text: str):
    """
    Match a resume against all jobs in the database.
    """

    # Extract skills from the resume
    resume_skills = set(get_resume_skills(resume_text))

    jobs = get_all_jobs(db)

    recommendations = []

    for job in jobs:
        # Extract skills from the job description
        job_skills = set(extract_skills(job["description"] or ""))

        # Skills present in both resume and job
        matched_skills = sorted(list(resume_skills & job_skills))

        # Skills required by the job but missing in the resume
        missing_skills = sorted(list(job_skills - resume_skills))

        # Calculate match score
        if len(job_skills) == 0:
            match_score = 0
        else:
            match_score = round(
                (len(matched_skills) / len(job_skills)) * 100,
                2
            )

        recommendations.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company_name"],
            "location": job["location_name"],
            "source": job["source_name"],
            "link": job["link"],
            "match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations[:10]