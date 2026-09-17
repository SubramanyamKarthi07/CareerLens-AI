def generate_career_summary(
    resume_score: float,
    strengths: list[str],
    weaknesses: list[str]
):
    """
    Generates an AI-style career summary.
    """

    # Career level
    if resume_score >= 90:
        level = "Advanced"
    elif resume_score >= 75:
        level = "Intermediate"
    elif resume_score >= 50:
        level = "Beginner"
    else:
        level = "Learning Stage"

    # Strongest areas
    if len(strengths) >= 3:
        strong_text = ", ".join(strengths[:3])
    elif strengths:
        strong_text = ", ".join(strengths)
    else:
        strong_text = "basic technical skills"

    # Areas to improve
    if weaknesses:
        improve_text = ", ".join(weaknesses[:3])
    else:
        improve_text = "advanced analytics and cloud technologies"

    summary = (
        f"You are currently at the {level} level as a Data Analyst candidate. "
        f"Your profile demonstrates strengths in {strong_text}. "
        f"To become more competitive for top Data Analyst roles, "
        f"consider improving your knowledge of {improve_text}."
    )

    return {
        "career_level": level,
        "summary": summary
    }