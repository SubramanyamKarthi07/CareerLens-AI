from api.repositories.skill_repository import extract_skills


def get_resume_skills(text: str):
    return extract_skills(text)