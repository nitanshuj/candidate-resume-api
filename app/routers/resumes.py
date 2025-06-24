from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.crud.resume import get_resume, get_resumes, create_resume, delete_resume
from app.core.database import get_db
from app.core.exceptions import ResumeNotFoundError
from app.core.logger import logger

router = APIRouter()

@router.post("/", response_model=schemas.Resume, status_code=status.HTTP_201_CREATED)
def create_resume_endpoint(resume: schemas.ResumeCreate, db: Session = Depends(get_db)):
    """Create a new resume."""
    logger.info(f"Creating new resume for candidate ID: {resume.candidate_id}")
    return create_resume(db, resume)

@router.get("/", response_model=List[schemas.Resume])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all resumes with pagination."""
    resumes = get_resumes(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(resumes)} resumes")
    return resumes

@router.get("/{resume_id}", response_model=schemas.Resume)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    """Get a specific resume by ID."""
    logger.info(f"Fetching resume with ID: {resume_id}")
    db_resume = get_resume(db, resume_id)
    if db_resume is None:
        raise ResumeNotFoundError(resume_id)
    return db_resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume_endpoint(resume_id: int, db: Session = Depends(get_db)):
    """Delete a resume by ID."""
    logger.info(f"Deleting resume with ID: {resume_id}")
    delete_resume(db, resume_id)
    return
