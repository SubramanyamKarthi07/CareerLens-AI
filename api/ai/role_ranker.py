
DATA_ANALYST_ROLES = [
    "data analyst",
    "business intelligence analyst",
    "bi analyst",
    "reporting analyst",
    "business analyst",
    "analytics analyst",
    "mis analyst"
]


def calculate_role_relevance(job_title: str) -> float:
    """Score job titles for a fresher targeting Data Analyst roles."""
    title = (job_title or "").lower().strip()

    if not title:
        return 0.0

    junior_roles = [
        "junior data analyst",
        "entry level data analyst",
        "entry-level data analyst",
        "data analyst intern",
        "data analytics intern",
        "graduate data analyst",
        "associate data analyst",
        "trainee data analyst"
    ]

    if any(role in title for role in junior_roles):
        return 100.0

    senior_roles = [
        "senior", "sr.", "lead", "principal",
        "staff", "director", "manager", "head of"
    ]

    if any(role in title for role in senior_roles):
        return 25.0

    if "data analyst" in title:
        return 90.0

    analyst_roles = [
        "business intelligence analyst",
        "bi analyst",
        "reporting analyst",
        "business analyst",
        "analytics analyst",
        "mis analyst"
    ]

    if any(role in title for role in analyst_roles):
        return 80.0

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


def calculate_location_relevance(
    job_location: str,
    job_description: str = ""
) -> float:
    """
    Prefer Chennai, then other Indian locations,
    then remote opportunities, followed by other locations.
    """
    location = (job_location or "").lower().strip()
    description = (job_description or "").lower()

    # Highest preference: Chennai
    if "chennai" in location:
        return 100.0

    # Other Indian locations
    indian_location_terms = [
        "india",
        "tamil nadu",
        "andhra pradesh",
        "telangana",
        "karnataka",
        "kerala",
        "maharashtra",
        "new delhi",
        "mumbai",
        "bengaluru",
        "bangalore",
        "hyderabad",
        "pune",
        "tirupati",
        "coimbatore"
    ]

    if any(term in location for term in indian_location_terms):
        return 80.0

    # Identify arrangements that are not fully remote
    hybrid_phrases = [
        "hybrid",
        "partially remote",
        "partly remote",
        "days onsite",
        "days on-site",
        "days in office",
        "in-office",
        "in office",
        "on-site",
        "onsite",
        "in-person"
    ]

    is_hybrid = any(
        phrase in description for phrase in hybrid_phrases
    )

    non_remote_phrases = [
        "not remote",
        "no remote work",
        "remote work is not available",
        "remote work unavailable",
        "not eligible for remote work"
    ]

    explicitly_non_remote = any(
        phrase in description for phrase in non_remote_phrases
    )

    if explicitly_non_remote:
        return 25.0

    if is_hybrid:
        return 60.0

    # Remote opportunities
    remote_location = (
        "remote" in location
        or "work from home" in location
        or "work-from-home" in location
    )

    full_remote_phrases = [
        "fully remote",
        "100% remote",
        "fully work from home",
        "work from home",
        "work-from-home"
    ]

    full_remote_description = any(
        phrase in description for phrase in full_remote_phrases
    )

    if remote_location or full_remote_description:
        return 70.0

    # Other international or unspecified locations
    return 30.0


def calculate_final_job_score(
    match_score: float,
    job_title: str,
    job_location: str = "",
    job_description: str = ""
) -> float:
    """
    Combine technical match, role relevance, and location preference.
    """
    relevance_score = calculate_role_relevance(job_title)

    location_score = calculate_location_relevance(
        job_location,
        job_description
    )

    final_score = (
        match_score * 0.75
        + relevance_score * 0.15
        + location_score * 0.10
    )

    return round(final_score, 2)
