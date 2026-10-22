
import time

from api.services.skill_service import get_resume_skills
from api.services.matching_service import match_resume_with_jobs
from api.services.roadmap_service import generate_roadmap_from_resume

from api.ai.resume_analyzer import analyze_resume
from api.ai.career_summary import generate_career_summary
from api.ai.strength_analyzer import generate_strengths
from api.ai.improvement_analyzer import analyze_improvement_areas


def generate_career_report(db, resume_text):
    """
    Generate a complete career report from a resume
    and print timing information for performance testing.
    """

    report_start = time.perf_counter()

    # 1. Extract resume skills
    start = time.perf_counter()
    resume_skills = get_resume_skills(resume_text)
    print(
        f"[TIMING] Resume skill extraction: "
        f"{time.perf_counter() - start:.2f}s"
    )

    # 2. Get job recommendations
    start = time.perf_counter()
    recommendations = match_resume_with_jobs(
        db,
        resume_text
    )
    print(
        f"[TIMING] Job matching: "
        f"{time.perf_counter() - start:.2f}s"
    )

    # 3. Generate learning roadmap
    start = time.perf_counter()
    roadmap = generate_roadmap_from_resume(
        db,
        resume_text,
        recommendations=recommendations
    )
    print(
        f"[TIMING] Roadmap generation: "
        f"{time.perf_counter() - start:.2f}s"
    )

    # 4. Analyze resume sections
    start = time.perf_counter()
    analysis = analyze_resume(resume_text)
    print(
        f"[TIMING] Resume analysis: "
        f"{time.perf_counter() - start:.2f}s"
    )

    text = (resume_text or "").lower()

    # -----------------------------
    # Resume Score Calculation
    # -----------------------------

    # 5. Technical Skills: Maximum 30 points
    skills_score = min(len(resume_skills) * 2.5, 30)

    # 6. Projects: Maximum 20 points
    project_score = 0

    if analysis["projects"] > 0:
        project_score = 10

        project_detail_keywords = [
            "developed",
            "built",
            "implemented",
            "designed",
            "achieved",
            "improved",
            "accuracy",
            "dashboard",
            "pipeline"
        ]

        detail_count = sum(
            1
            for keyword in project_detail_keywords
            if keyword in text
        )

        project_score += min(detail_count * 2, 10)

    # 7. Experience: Maximum 20 points
    experience_score = 0

    if analysis["experience"] > 0:
        experience_score = 10

        impact_keywords = [
            "responsible for",
            "managed",
            "analyzed",
            "automated",
            "reduced",
            "increased",
            "improved",
            "delivered",
            "%"
        ]

        impact_count = sum(
            1
            for keyword in impact_keywords
            if keyword in text
        )

        experience_score += min(impact_count * 2, 10)

    # 8. Education: Maximum 15 points
    education_score = (
        15 if analysis["education"] > 0 else 0
    )

    # 9. Certifications: Maximum 5 points
    certification_score = (
        5 if analysis["certifications"] > 0 else 0
    )

    # 10. Resume Content and Structure: Maximum 10 points
    structure_keywords = [
        "summary",
        "skills",
        "education",
        "experience",
        "projects"
    ]

    sections_found = sum(
        1
        for section in structure_keywords
        if section in text
    )

    structure_score = min(sections_found * 2, 10)

    # 11. Calculate final resume score
    resume_score = round(
        skills_score
        + project_score
        + experience_score
        + education_score
        + certification_score
        + structure_score,
        2
    )

    resume_score = min(resume_score, 100)

    # 12. Generate strengths, weaknesses, and career summary
    start = time.perf_counter()

    strengths = generate_strengths(resume_skills)

    weaknesses = analyze_improvement_areas(
        resume_text=resume_text,
        resume_skills=resume_skills,
        recommendations=recommendations
    )

    career_summary = generate_career_summary(
        resume_score,
        strengths,
        weaknesses,
        resume_text
    )

    print(
        f"[TIMING] Strengths/weaknesses/summary: "
        f"{time.perf_counter() - start:.2f}s"
    )

    # 13. Print total report generation time
    print(
        f"[TIMING] Total report generation: "
        f"{time.perf_counter() - report_start:.2f}s"
    )

    # 14. Return complete career report
    return {
        "resume_score": resume_score,
        "career_level": career_summary["career_level"],
        "career_summary": career_summary["summary"],
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations,
        "roadmap": roadmap
    }
