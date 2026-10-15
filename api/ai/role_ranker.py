
DATA_ANALYST_ROLES = [
    "data analyst",
    "junior data analyst",
    "business intelligence analyst",
    "bi analyst",
    "reporting analyst",
    "business analyst",
    "analytics analyst",
    "mis analyst"
]


def calculate_role_relevance(job_title: str) -> float:
    """
    Return a role relevance score between 0 and 100
    for a Data Analyst career path.
    """
    title = job_title.lower().strip()

    if not title:
        return 0.0

    if any(role in title for role in DATA_ANALYST_ROLES):
        return 100.0

    related_roles = [
        "data scientist",
        "analytics engineer",
        "business intelligence",
        "data engineer",
        "machine learning"
    ]

    if any(role in title for role in related_roles):
        return 60.0

    return 30.0


def calculate_final_job_score(
    match_score: float,
    job_title: str
) -> float:
    """
    Combine technical match and career-role relevance.
    """
    relevance_score = calculate_role_relevance(job_title)

    final_score = (
        match_score * 0.85
        + relevance_score * 0.15
    )

    return round(final_score, 2)
