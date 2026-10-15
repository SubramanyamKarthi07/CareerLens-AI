
def analyze_improvement_areas(
    resume_text: str,
    resume_skills: list[str],
    recommendations: list[dict]
) -> list[str]:
    """
    Identify practical resume and career improvement areas
    using basic keyword checks and job-specific skill gaps.
    """
    text = resume_text.lower()
    skills = {skill.lower() for skill in resume_skills}
    improvements = []

    # 1. Identify job-specific skill gaps across the top five jobs
    missing_skills = set()

    for job in recommendations[:5]:
        for skill in job.get("missing_skills", []):
            normalized_skill = skill.strip().lower()
            if normalized_skill and normalized_skill not in skills:
                missing_skills.add(normalized_skill)

    if missing_skills:
        improvements.append(
            "Prioritize learning or demonstrating these skills for "
            "your target roles: "
            + ", ".join(sorted(missing_skills)[:5])
            + "."
        )

    # 2. Check for project evidence
    has_projects = "project" in text
    project_action_keywords = [
        "developed", "built", "implemented",
        "designed", "automated", "analyzed"
    ]

    has_project_actions = any(
        keyword in text for keyword in project_action_keywords
    )

    if not has_projects:
        improvements.append(
            "Add a dedicated projects section featuring relevant "
            "data analytics projects."
        )
    elif not has_project_actions:
        improvements.append(
            "Describe your project contributions using specific actions, "
            "tools, and problems solved."
        )

    # 3. Check for evidence of measurable impact
    impact_keywords = [
        "increased", "reduced", "improved", "saved",
        "achieved", "accuracy", "%"
    ]

    has_impact_evidence = any(
        keyword in text for keyword in impact_keywords
    )

    if not has_impact_evidence:
        improvements.append(
            "Where supported by evidence, quantify project or internship "
            "outcomes, such as time saved, records processed, or accuracy."
        )

    # 4. Check for practical experience
    experience_keywords = [
        "internship", "intern", "work experience",
        "employment", "professional experience"
    ]

    if not any(keyword in text for keyword in experience_keywords):
        improvements.append(
            "Highlight relevant internship, practical work, or experience "
            "with clear responsibilities."
        )

    # 5. Check for certifications
    certification_keywords = [
        "certification", "certifications",
        "certified", "certificate"
    ]

    if not any(keyword in text for keyword in certification_keywords):
        improvements.append(
            "Include relevant certifications you have completed, if applicable."
        )

    # 6. Actionable fallback when no gaps are detected
    if not improvements:
        improvements.append(
            "Review your resume against each target job description. "
            "Prioritize relevant skills and make project contributions "
            "and outcomes clear, accurate, and easy to verify."
        )

    return improvements
