
import time

from sqlalchemy.orm import Session

from api.services.skill_service import get_resume_skills
from api.repositories.matching_repository import get_all_jobs
from api.repositories.skill_repository import extract_skills
from api.ai.weighted_matcher import calculate_weighted_score
from api.ai.career_advisor import generate_recommendation
from api.ai.role_ranker import calculate_final_job_score


def match_resume_with_jobs(db: Session, resume_text: str):
    total_start = time.perf_counter()

    # 1. Extract resume skills
    start = time.perf_counter()
    resume_skills = set(get_resume_skills(resume_text))
    print(
        f"[MATCH TIMING] Resume skills: "
        f"{time.perf_counter() - start:.2f}s"
    )

    # 2. Fetch jobs from the database
    start = time.perf_counter()
    jobs = get_all_jobs(db)
    print(
        f"[MATCH TIMING] Database fetch: "
        f"{time.perf_counter() - start:.2f}s "
        f"({len(jobs)} jobs)"
    )

    # 3. Score and rank jobs
    scoring_start = time.perf_counter()
    recommendations = []
    extraction_time = 0.0
    scoring_time = 0.0
    recommendation_time = 0.0

    for job in jobs:
        start = time.perf_counter()
        job_skills = set(
            extract_skills(job["description"] or "")
        )
        extraction_time += time.perf_counter() - start

        if not job_skills:
            continue

        start = time.perf_counter()
        match_score, matched_skills, missing_skills = (
            calculate_weighted_score(
                resume_skills,
                job_skills
            )
        )

        final_score = calculate_final_job_score(
            match_score=match_score,
            job_title=job["title"] or "",
            job_location=job["location_name"] or "",
            job_description=job["description"] or ""
        )
        scoring_time += time.perf_counter() - start

        if final_score < 25:
            continue

        start = time.perf_counter()
        recommendation = generate_recommendation(
            missing_skills
        )
        recommendation_time += time.perf_counter() - start

        recommendations.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company_name"],
            "location": job["location_name"],
            "source": job["source_name"],
            "link": job["link"],
            "match_score": final_score,
            "technical_match_score": match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendation": recommendation
        })

    print(
        f"[MATCH TIMING] Job skill extraction: "
        f"{extraction_time:.2f}s"
    )
    print(
        f"[MATCH TIMING] Scoring and ranking: "
        f"{scoring_time:.2f}s"
    )
    print(
        f"[MATCH TIMING] Recommendation generation: "
        f"{recommendation_time:.2f}s"
    )

    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )

    result = recommendations[:10]

    print(
        f"[MATCH TIMING] Total matching: "
        f"{time.perf_counter() - total_start:.2f}s"
    )

    return result
