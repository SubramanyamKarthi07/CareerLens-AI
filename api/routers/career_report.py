import os
import shutil

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)
from sqlalchemy.orm import Session

from api.database import get_db
from api.schemas import CareerReportResponse
from api.services.resume_service import parse_resume
from api.services.career_report_service import generate_career_report

router = APIRouter(
    prefix="/career",
    tags=["Career Report"]
)


@router.post(
    "/report",
    response_model=CareerReportResponse
)
async def career_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Generate a complete AI-powered career report from a resume.
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

    report = generate_career_report(
        db,
        resume_text
    )

    return report