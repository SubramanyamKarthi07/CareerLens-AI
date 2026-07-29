from api.skills_database import SKILLS


def extract_skills(text: str):
    """
    Extracts normalized skills from resume text.
    """

    text = text.lower()

    extracted_skills = set()

    for skill, keywords in SKILLS.items():

        for keyword in keywords:

            if keyword.lower() in text:
                extracted_skills.add(skill)
                break

    return sorted(list(extracted_skills))