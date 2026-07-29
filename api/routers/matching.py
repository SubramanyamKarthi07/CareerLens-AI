from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import shutil

from api.database import get_db
from api.services.resume_service import parse_resume
from api.services.matching_service import match_resume_with_jobs
from api.schemas import ResumeMatchingResponse

router = APIRouter(
    prefix="/matching",
    tags=["Job Matching"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post(
    "/resume",
    response_model=list[ResumeMatchingResponse]
)
async def match_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    extension = Path(file.filename).suffix.lower()

    if extension not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = parse_resume(str(file_path))

    recommendations = match_resume_with_jobs(db, resume_text)

    return recommendations