
def generate_career_summary(
    resume_score: float,
    strengths: list[str],
    weaknesses: list[str],
    resume_text: str = ""
):
    """
    Generate a career summary using resume quality,
    experience evidence, strengths, and improvement areas.
    """

    text = resume_text.lower()

    # Determine career level using experience evidence,
    # rather than resume score alone.
    experience_keywords = [
        "internship",
        "intern",
        "full-time",
        "full time",
        "professional experience",
        "work experience",
        "years of experience",
        "employment history"
    ]

    has_experience = any(
        keyword in text for keyword in experience_keywords
    )

    if has_experience:
        level = "Early-Career Professional"
    elif resume_score >= 75:
        level = "Career-Ready Candidate"
    elif resume_score >= 50:
        level = "Developing Candidate"
    else:
        level = "Learning Stage"

    # Summarize strengths
    if len(strengths) >= 3:
        strong_text = ", ".join(strengths[:3])
    elif strengths:
        strong_text = ", ".join(strengths)
    else:
        strong_text = "foundational technical skills"

    # Handle improvement suggestions
    if weaknesses:
        improvement_text = " ".join(
            item.strip().rstrip(".")
            for item in weaknesses[:2]
            if item.strip()
        )
        improvement_text += "."
    else:
        improvement_text = (
            "Continue tailoring your resume to target roles "
            "and highlighting verified project outcomes."
        )

    summary = (
        f"Your current career classification is {level}. "
        f"Your resume-quality score is {resume_score}/100. "
        f"Your profile demonstrates strengths in {strong_text}. "
        f"Recommended next steps: {improvement_text}"
    )


    return {
        "career_level": level,
        "summary": summary
    }
