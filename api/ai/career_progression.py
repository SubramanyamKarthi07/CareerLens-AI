CAREER_PATH = [
    "excel",
    "sql",
    "python",
    "statistics",
    "power bi",
    "tableau",
    "git",
    "github",
    "machine learning",
    "scikit-learn",
    "docker",
    "aws"
]


def recommend_next_skills(resume_skills):
    """
    Recommend the next skills to learn based on the user's current skills.
    """

    resume_skills = {skill.lower() for skill in resume_skills}

    next_skills = []

    for skill in CAREER_PATH:
        if skill not in resume_skills:
            next_skills.append(skill)

    return next_skills[:5]