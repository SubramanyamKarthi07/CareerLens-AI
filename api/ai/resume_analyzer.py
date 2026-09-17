import re


def analyze_resume(resume_text: str):
    """
    Analyze the resume and return feature scores.
    """

    text = resume_text.lower()

    result = {
        "projects": 0,
        "experience": 0,
        "education": 0,
        "certifications": 0
    }

    # Projects
    if "project" in text or "projects" in text:
        result["projects"] = 20

    # Experience
    experience_keywords = [
        "experience",
        "intern",
        "internship",
        "worked",
        "employment"
    ]

    if any(word in text for word in experience_keywords):
        result["experience"] = 20

    # Education
    education_keywords = [
        "b.tech",
        "bachelor",
        "degree",
        "college",
        "university"
    ]

    if any(word in text for word in education_keywords):
        result["education"] = 10

    # Certifications
    certification_keywords = [
        "certificate",
        "certification",
        "certified"
    ]

    if any(word in text for word in certification_keywords):
        result["certifications"] = 10

    return result