
CAREER_PATH = [
    "sql",
    "power query",
    "dax",
    "data modeling",
    "query optimization",
    "excel",
    "power bi",
    "tableau",
    "statistics",
    "exploratory data analysis",
    "data visualization",
    "pandas",
    "numpy",
    "machine learning",
    "docker",
    "aws",
]


def recommend_next_skills(resume_skills):
    """
    Recommend next learning priorities for a Data Analyst.
    Skip skills already detected in the resume.
    """

    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    next_skills = [
        skill
        for skill in CAREER_PATH
        if skill not in resume_skills
    ]

    return next_skills[:5]
