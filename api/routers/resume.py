from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os

from api.services.resume_service import parse_resume
from api.services.skill_service import get_resume_skills

from api.schemas import ResumeAnalysisResponse
from api.ai.resume_scorer import score_resume
from api.schemas import ResumeScoreResponse
from api.ai.resume_scorer_v2 import score_resume_v2

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

@router.post("/score", response_model=ResumeScoreResponse)
async def score_uploaded_resume(file: UploadFile = File(...)):
    """
    Upload a resume and generate an overall resume score.
    """

    allowed_extensions = (".pdf", ".docx")

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = parse_resume(file_path)

    resume_skills = get_resume_skills(resume_text)

    return score_resume(resume_skills)

@router.post("/score-v2", response_model=ResumeScoreResponse)
async def score_uploaded_resume_v2(file: UploadFile = File(...)):
    """
    Upload a resume and generate a category-based resume score.
    """

    allowed_extensions = (".pdf", ".docx")

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = parse_resume(file_path)

    resume_skills = get_resume_skills(resume_text)

    return score_resume_v2(resume_skills)