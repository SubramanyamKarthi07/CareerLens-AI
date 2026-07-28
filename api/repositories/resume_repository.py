import fitz
from docx import Document
from pathlib import Path


def extract_resume_text(file_path: str):
    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    raise ValueError("Unsupported file format")


def extract_pdf(file_path: str):
    text = ""

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()

    return text


def extract_docx(file_path: str):
    document = Document(file_path)
    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
    )