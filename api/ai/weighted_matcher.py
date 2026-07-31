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
    Calculate weighted match score between resume skills and job skills.

    Returns:
        score (float)
        matched_skills (list)
        missing_skills (list)
    """

    resume_skills = set(resume_skills)
    job_skills = set(job_skills)

    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    total_weight = 0
    matched_weight = 0

    for skill in job_skills:
        weight = SKILL_WEIGHTS.get(skill.lower(), 5)
        total_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    score = 0

    if total_weight > 0:
        score = round((matched_weight / total_weight) * 100, 2)

    return score, matched_skills, missing_skills