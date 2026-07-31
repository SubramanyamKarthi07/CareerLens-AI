from sqlalchemy.orm import Session

from api.services.skill_service import get_resume_skills
from api.repositories.matching_repository import get_all_jobs
from api.repositories.skill_repository import extract_skills
from api.ai.weighted_matcher import calculate_weighted_score
from api.ai.career_advisor import generate_recommendation


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

        # Calculate weighted match score
        match_score, matched_skills, missing_skills = calculate_weighted_score(
            resume_skills,
            job_skills
        )

        # Generate recommendation
        recommendation = generate_recommendation(missing_skills)

        recommendations.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company_name"],
            "location": job["location_name"],
            "source": job["source_name"],
            "link": job["link"],
            "match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendation": recommendation
        })
    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    return recommendations[:10]