"""CRUD operations for candidates."""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status

from app.models.candidate import Candidate
from app.schemas import CandidateCreate
from app.core.exceptions import CandidateNotFoundError, EmailAlreadyExistsError
from app.core.logger import logger

def get_candidate(db: Session, candidate_id: int):
    """Get a candidate by ID."""
    candidate = db.query(Candidate).filter(Candidate.candidate_id == candidate_id).first()
    if not candidate:
        logger.warning(f"Candidate with ID {candidate_id} not found")
    return candidate

def get_candidate_by_email(db: Session, email: str):
    """Get a candidate by email."""
    return db.query(Candidate).filter(Candidate.email == email).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    """Get multiple candidates with pagination."""
    logger.debug(f"Fetching candidates (skip={skip}, limit={limit})")
    return db.query(Candidate).offset(skip).limit(limit).all()

def create_candidate(db: Session, candidate: CandidateCreate):
    """Create a new candidate."""
    db_candidate = Candidate(**candidate.dict())
    db.add(db_candidate)
    try:
        db.commit()
        db.refresh(db_candidate)
        logger.info(f"Created candidate with ID {db_candidate.candidate_id}")
        return db_candidate
    except IntegrityError:
        db.rollback()
        logger.warning(f"Attempt to create candidate with duplicate email: {candidate.email}")
        raise EmailAlreadyExistsError()

def delete_candidate(db: Session, candidate_id: int):
    """Delete a candidate by ID."""
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise CandidateNotFoundError(candidate_id)
    
    db.delete(candidate)
    db.commit()
    logger.info(f"Deleted candidate with ID {candidate_id}")
    return None
