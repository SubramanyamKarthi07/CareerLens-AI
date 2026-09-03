def generate_learning_roadmap(missing_skills):
    """
    Generate a simple week-by-week learning roadmap
    based on missing skills.
    """

    roadmap = []

    week = 1

    for skill in missing_skills:
        roadmap.append({
            "week": week,
            "focus": skill,
            "goal": f"Learn the fundamentals of {skill}.",
            "practice": f"Complete at least one hands-on project using {skill}."
        })
        week += 1

    if not roadmap:
        roadmap.append({
            "week": 1,
            "focus": "Advanced Projects",
            "goal": "Build portfolio-ready projects.",
            "practice": "Apply for jobs and continue improving your portfolio."
        })

    return roadmap