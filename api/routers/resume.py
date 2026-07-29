from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from api.services.resume_service import parse_resume
from api.services.skill_service import get_resume_skills

from api.schemas import ResumeAnalysisResponse

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post(
    "/analyze",
    response_model=ResumeAnalysisResponse
)
async def analyze_resume(file: UploadFile = File(...)):

    extension = Path(file.filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = parse_resume(str(file_path))

    skills = get_resume_skills(extracted_text)

    return {
        "filename": file.filename,
        "characters": len(extracted_text),
        "skills": skills,
        "preview": extracted_text[:500]
    }