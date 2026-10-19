
def analyze_improvement_areas(
    resume_text: str,
    resume_skills: list[str],
    recommendations: list[dict]
) -> list[str]:
    """
    Identify practical resume and career improvement areas
    using resume evidence and recommended-job skill gaps.
    """
    text = (resume_text or "").lower()
    skills = {
        skill.strip().lower()
        for skill in (resume_skills or [])
        if skill and skill.strip()
    }

    improvements = []

    # 1. Identify skill gaps across the top five recommendations
    missing_skill_counts = {}

    for job in (recommendations or []):
        for skill in job.get("missing_skills") or []:
            normalized_skill = skill.strip().lower()

            if normalized_skill and normalized_skill not in skills:
                missing_skill_counts[normalized_skill] = (
                    missing_skill_counts.get(normalized_skill, 0) + 1
                )

    # Prioritize skills appearing in multiple recommended jobs
    if missing_skill_counts:
        ranked_missing_skills = sorted(
            missing_skill_counts,
            key=lambda skill: (-missing_skill_counts[skill], skill)
        )

        improvements.append(
            "Consider developing or demonstrating these skills "
            "requested by your recommended jobs: "
            + ", ".join(ranked_missing_skills[:5])
            + ". Verify each job's requirements before prioritizing."
        )

    # 2. Check project evidence
    has_projects = any(
        keyword in text
        for keyword in ["project", "projects"]
    )

    project_action_keywords = [
        "developed", "built", "implemented",
        "designed", "automated", "analyzed"
    ]

    if not has_projects:
        improvements.append(
            "Add a dedicated projects section featuring relevant "
            "data analytics projects, the tools used, and the problem solved."
        )
    elif not any(keyword in text for keyword in project_action_keywords):
        improvements.append(
            "Strengthen project descriptions with specific actions, "
            "tools, and problems solved."
        )

    # 3. Check measurable outcomes
    impact_keywords = [
        "increased", "reduced", "improved", "saved",
        "achieved", "accuracy", "%"
    ]

    if not any(keyword in text for keyword in impact_keywords):
        improvements.append(
            "Where evidence is available, quantify project or internship "
            "outcomes, such as records processed, time saved, or accuracy. "
            "Do not invent metrics."
        )

    # 4. Check practical experience
    experience_keywords = [
        "internship", "intern", "work experience",
        "employment", "professional experience"
    ]

    if not any(keyword in text for keyword in experience_keywords):
        improvements.append(
            "Highlight relevant internships or practical experience, "
            "including your responsibilities and contributions."
        )

    # 5. Check certifications
    certification_keywords = [
        "certification", "certifications",
        "certified", "certificate"
    ]

    if not any(keyword in text for keyword in certification_keywords):
        improvements.append(
            "List relevant certifications you have completed, if applicable."
        )

    # 6. Provide useful feedback if no specific issue was detected
    if not improvements:
        improvements.append(
            "Your resume passed the current basic checks. For a more "
            "targeted review, compare its project evidence and demonstrated "
            "skills with the requirements of your preferred job descriptions."
        )

    return improvements
