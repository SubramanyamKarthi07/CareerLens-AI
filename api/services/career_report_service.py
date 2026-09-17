from api.services.skill_service import get_resume_skills
from api.services.matching_service import match_resume_with_jobs
from api.services.roadmap_service import generate_roadmap_from_resume
from api.ai.resume_analyzer import analyze_resume
from api.ai.career_summary import generate_career_summary
from api.ai.strength_analyzer import generate_strengths

def generate_career_report(db, resume_text):
    """
    Generate a complete career report from a resume.
    """

    # Extract resume skills
    resume_skills = get_resume_skills(resume_text)

    # Get job recommendations
    recommendations = match_resume_with_jobs(
        db,
        resume_text
    )

    # Generate learning roadmap
    roadmap = generate_roadmap_from_resume(
        db,
        resume_text
    )

    # -----------------------------
    # Resume Score Calculation
    # -----------------------------
    analysis = analyze_resume(resume_text)

    # Skills Score (Maximum 40)
    skills_score = min(len(resume_skills) * 4, 40)

    resume_score = (
        skills_score
        + analysis["projects"]
        + analysis["experience"]
        + analysis["education"]
        + analysis["certifications"]
    )

    resume_score = min(resume_score, 100)

  
    # Professional Strengths
    strengths = generate_strengths(resume_skills)

    # Weaknesses
    if recommendations:
        weaknesses = recommendations[0]["missing_skills"]
    else:
        weaknesses = []

    # Generate AI Summary
    career_summary = generate_career_summary(
        resume_score,
        strengths,
        weaknesses
    )

    return {
        "resume_score": resume_score,
        "career_level": career_summary["career_level"],
        "career_summary": career_summary["summary"],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "roadmap": roadmap
    }