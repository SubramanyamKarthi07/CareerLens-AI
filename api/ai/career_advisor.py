def generate_recommendation(missing_skills):
    """
    Generate personalized advice based on missing skills.
    """

    if not missing_skills:
        return (
            "Excellent match! Your resume already covers the key skills "
            "required for this role."
        )

    if len(missing_skills) == 1:
        return (
            f"Learning {missing_skills[0]} could significantly improve "
            "your match for this position."
        )

    if len(missing_skills) <= 3:
        skills = ", ".join(missing_skills[:-1]) + f" and {missing_skills[-1]}"
        return (
            f"Consider learning {skills} to strengthen your profile for this role."
        )

    return (
        "Several important skills are missing. Focus on the highest-priority "
        "technical skills to improve your chances."
    )