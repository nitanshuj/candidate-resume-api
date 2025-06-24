"""CRUD operations for resumes."""
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.schemas import ResumeCreate
from app.core.exceptions import ResumeNotFoundError, CandidateNotFoundError
from app.crud.candidate import get_candidate
from app.core.logger import logger

def get_resume(db: Session, resume_id: int):
    """Get a resume by ID."""
    resume = db.query(Resume).filter(Resume.resume_id == resume_id).first()
    if not resume:
        logger.warning(f"Resume with ID {resume_id} not found")
    return resume

def get_resumes(db: Session, skip: int = 0, limit: int = 100):
    """Get multiple resumes with pagination."""
    logger.debug(f"Fetching resumes (skip={skip}, limit={limit})")
    return db.query(Resume).offset(skip).limit(limit).all()

def create_resume(db: Session, resume: ResumeCreate):
    """Create a new resume."""
    candidate = get_candidate(db, resume.candidate_id)
    if not candidate:
        logger.warning(f"Attempt to create resume for non-existent candidate ID: {resume.candidate_id}")
        raise CandidateNotFoundError(resume.candidate_id)
    
    db_resume = Resume(**resume.dict())
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    logger.info(f"Created resume with ID {db_resume.resume_id} for candidate {resume.candidate_id}")
    return db_resume

def delete_resume(db: Session, resume_id: int):
    """Delete a resume by ID."""
    resume = get_resume(db, resume_id)
    if not resume:
        raise ResumeNotFoundError(resume_id)
    
    db.delete(resume)
    db.commit()
    logger.info(f"Deleted resume with ID {resume_id}")
    return None
