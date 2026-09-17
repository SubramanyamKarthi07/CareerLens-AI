SKILL_WEIGHTS = {
    "python": 10,
    "sql": 10,
    "machine learning": 9,
    "deep learning": 9,
    "data analysis": 8,
    "power bi": 8,
    "tableau": 8,
    "statistics": 8,
    "pandas": 7,
    "numpy": 7,
    "excel": 6,
    "tensorflow": 6,
    "scikit-learn": 6,
    "git": 3,
    "github": 3
}


def calculate_weighted_score(resume_skills, job_skills):
    """
    Calculate an intelligent weighted match score.

    Returns:
        score (float)
        matched_skills (list)
        missing_skills (list)
    """

    resume_skills = {skill.lower() for skill in resume_skills}
    job_skills = {skill.lower() for skill in job_skills}

    matched_skills = sorted(list(resume_skills & job_skills))
    missing_skills = sorted(list(job_skills - resume_skills))

    total_job_weight = 0
    matched_weight = 0

    # Weight based on job requirements
    for skill in job_skills:
        weight = SKILL_WEIGHTS.get(skill, 5)
        total_job_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    # Required Skill Match (70%)
    if total_job_weight == 0:
        required_match = 0
    else:
        required_match = (matched_weight / total_job_weight) * 100

    # Resume Coverage (30%)
    if len(resume_skills) == 0:
        coverage = 0
    else:
        coverage = (len(matched_skills) / len(resume_skills)) * 100

    # Final weighted score
    score = round(
        (required_match * 0.7) +
        (coverage * 0.3),
        2
    )

    return score, matched_skills, missing_skills