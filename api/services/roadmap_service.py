from api.ai.roadmap_generator import generate_learning_roadmap
from api.services.matching_service import match_resume_with_jobs
from api.services.skill_service import get_resume_skills
from api.ai.career_progression import recommend_next_skills


def get_learning_roadmap(missing_skills):
    """
    Generate a learning roadmap based on missing skills.
    """
    return generate_learning_roadmap(missing_skills)


def generate_roadmap_from_resume(db, resume_text):
    """
    Generate a personalized learning roadmap using resume skills
    and skill gaps from relevant job recommendations.
    """

    # 1. Extract the candidate's existing skills
    resume_skills = get_resume_skills(resume_text)
    resume_skill_set = {
        skill.lower().strip() for skill in resume_skills
    }

    # 2. Get recommended jobs using the existing matching service
    recommendations = match_resume_with_jobs(db, resume_text)


    # 3. Collect missing skills from the top Data Analyst-related jobs
    job_missing_skills = []

    for job in recommendations[:5]:
        for skill in job.get("missing_skills", []):
            normalized_skill = skill.lower().strip()

            if (
                normalized_skill
                and normalized_skill not in resume_skill_set
                and normalized_skill not in job_missing_skills
            ):
                job_missing_skills.append(normalized_skill)

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
        skill for skill in priority_skills
        if skill in job_missing_skills
    ]

    # 5. Add other job-specific missing skills
    remaining_missing = [
        skill for skill in job_missing_skills
        if skill not in prioritized_missing
    ]

    # 6. Fill remaining spaces with career progression skills
    progression_skills = recommend_next_skills(resume_skills)

    combined_skills = (
        prioritized_missing
        + remaining_missing
        + [
            skill.lower().strip()
            for skill in progression_skills
            if skill.lower().strip() not in job_missing_skills
        ]
    )

    # Keep the roadmap focused and avoid duplicate skills
    unique_skills = list(dict.fromkeys(combined_skills))
    next_skills = unique_skills[:5]

    # 7. Generate the four-week roadmap
    return generate_learning_roadmap(next_skills)
