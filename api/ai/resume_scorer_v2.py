CATEGORY_WEIGHTS = {
    "Programming": 25,
    "Databases": 20,
    "Visualization": 20,
    "Data Analysis": 15,
    "Machine Learning": 10,
    "Version Control": 5,
    "Statistics": 5
}


CATEGORY_SKILLS = {
    "Programming": [
        "python"
    ],

    "Databases": [
        "sql"
    ],

    "Visualization": [
        "power bi",
        "tableau",
        "excel"
    ],

    "Data Analysis": [
        "pandas",
        "numpy",
        "data analysis"
    ],

    "Machine Learning": [
        "machine learning",
        "deep learning",
        "scikit-learn",
        "tensorflow"
    ],

    "Version Control": [
        "git",
        "github"
    ],

    "Statistics": [
        "statistics"
    ]
}


def score_resume_v2(resume_skills):
    """
    Category-based resume scoring.
    """

    resume_skills = set(skill.lower() for skill in resume_skills)

    score = 0

    strengths = []
    areas_to_improve = []

    for category, skills in CATEGORY_SKILLS.items():

        found = False

        for skill in skills:

            if skill in resume_skills:

                found = True

                strengths.append(skill)

        if found:
            score += CATEGORY_WEIGHTS[category]
        else:
            areas_to_improve.append(category)

    if score >= 85:
        summary = (
            "Excellent resume. Your profile is well aligned for Data Analyst roles."
        )

    elif score >= 70:
        summary = (
            "Strong resume. Improving the missing categories will make your profile even more competitive."
        )

    elif score >= 50:
        summary = (
            "Good foundation. Focus on the missing categories to strengthen your resume."
        )

    else:
        summary = (
            "Your resume requires significant improvement for Data Analyst positions."
        )

    return {
        "resume_score": score,
        "strengths": sorted(strengths),
        "areas_to_improve": areas_to_improve,
        "summary": summary
    }