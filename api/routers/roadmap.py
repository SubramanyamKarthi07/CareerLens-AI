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
from api.schemas import RoadmapResponse
from api.services.resume_service import parse_resume
from api.services.roadmap_service import generate_roadmap_from_resume

router = APIRouter(
    prefix="/roadmap",
    tags=["Learning Roadmap"]
)


@router.post(
    "/generate",
    response_model=RoadmapResponse
)
async def generate_roadmap(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Generate a learning roadmap from an uploaded resume.
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

    roadmap = generate_roadmap_from_resume(
        db,
        resume_text
    )

    return {
        "roadmap": roadmap
    }
def generate_roadmap(
    missing_skills: list[str]
):
    """
    Generate a learning roadmap based on missing skills.
    """

    roadmap = get_learning_roadmap(missing_skills)

    return {
        "roadmap": roadmap
    }