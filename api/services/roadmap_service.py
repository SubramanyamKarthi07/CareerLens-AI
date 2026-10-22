
from api.ai.roadmap_generator import generate_learning_roadmap
from api.services.matching_service import match_resume_with_jobs
from api.services.skill_service import get_resume_skills
from api.ai.career_progression import recommend_next_skills


def get_learning_roadmap(missing_skills):
    """
    Generate a learning roadmap based on missing skills.
    """
    return generate_learning_roadmap(missing_skills)


def generate_roadmap_from_resume(
    db,
    resume_text,
    recommendations=None
):
    """
    Generate a personalized learning roadmap using resume skills
    and skill gaps from relevant job recommendations.

    Reuses existing recommendations when supplied to avoid
    running job matching twice for the same career report.
    """

    # 1. Extract the candidate's existing skills
    resume_skills = get_resume_skills(resume_text)

    resume_skill_set = {
        skill.lower().strip()
        for skill in resume_skills
    }

    # 2. Reuse recommendations if already calculated
    if recommendations is None:
        recommendations = match_resume_with_jobs(
            db,
            resume_text
        )

    # 3. Collect missing skills from the top 5 recommendations
    job_missing_skills = []
    seen_missing_skills = set()

    for job in recommendations[:5]:
        for skill in job.get("missing_skills", []):
            normalized_skill = skill.lower().strip()

            if (
                normalized_skill
                and normalized_skill not in resume_skill_set
                and normalized_skill not in seen_missing_skills
            ):
                job_missing_skills.append(normalized_skill)
                seen_missing_skills.add(normalized_skill)

    # 4. Prioritize common Data Analyst skills
    priority_skills = [
        "sql",
        "excel",
        "python",
        "statistics",
        "power bi",
        "tableau",
        "pandas",
        "numpy",
        "data analysis",
        "data visualization",
    ]

    prioritized_missing = [
        skill
        for skill in priority_skills
        if skill in seen_missing_skills
    ]

    # 5. Add other job-specific missing skills
    remaining_missing = [
        skill
        for skill in job_missing_skills
        if skill not in prioritized_missing
    ]

    # 6. Add career progression skills
    progression_skills = recommend_next_skills(resume_skills)

    combined_skills = (
        prioritized_missing
        + remaining_missing
        + [
            skill.lower().strip()
            for skill in progression_skills
            if skill.lower().strip()
            and skill.lower().strip() not in seen_missing_skills
        ]
    )

    # 7. Remove duplicates and select up to five skills
    unique_skills = list(dict.fromkeys(combined_skills))
    next_skills = unique_skills[:5]

    # 8. Generate the four-week roadmap
    return generate_learning_roadmap(next_skills)
