from api.ai.weighted_matcher import SKILL_WEIGHTS


def score_resume(resume_skills):
    """
    Generate an overall resume score based on extracted skills.
    """

    resume_skills = set(skill.lower() for skill in resume_skills)

    total_possible = sum(SKILL_WEIGHTS.values())

    earned = 0

    strengths = []
    areas_to_improve = []

    for skill, weight in SKILL_WEIGHTS.items():

        if skill in resume_skills:
            earned += weight
            strengths.append(skill)
        else:
            areas_to_improve.append(skill)

    resume_score = round((earned / total_possible) * 100, 2)

    if resume_score >= 85:
        summary = (
            "Excellent resume with strong technical skills."
        )

    elif resume_score >= 70:
        summary = (
            "Good resume. Adding a few more in-demand skills will improve your profile."
        )

    elif resume_score >= 50:
        summary = (
            "Average resume. Focus on learning important technical skills."
        )

    else:
        summary = (
            "Resume needs significant improvement for competitive Data Analyst roles."
        )

    return {
        "resume_score": resume_score,
        "strengths": strengths,
        "areas_to_improve": areas_to_improve,
        "summary": summary
    }