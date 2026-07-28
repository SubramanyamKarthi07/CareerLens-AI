from api.repositories.resume_repository import extract_resume_text


def parse_resume(file_path: str):
    return extract_resume_text(file_path)