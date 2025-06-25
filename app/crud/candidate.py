"""CRUD operations for candidates."""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status

from app.models.candidate import Candidate
from app.schemas import CandidateCreate, CandidateUpdate
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
    """
    Create a new candidate in the database.
    Handles duplicate emails gracefully.
    """
    try:
        # Check if email already exists
        existing_candidate = db.query(Candidate).filter(
            Candidate.email == candidate.email
        ).first()
        
        if existing_candidate:
            logger.warning(f"Attempt to create candidate with duplicate email: {candidate.email}")
            raise EmailAlreadyExistsError(email=candidate.email)
        
        # Create new candidate
        db_candidate = Candidate(**candidate.model_dump())  # Updated from .dict()
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)
        logger.info(f"Created candidate with ID {db_candidate.candidate_id}")
        return db_candidate
    
    except IntegrityError as e:
        db.rollback()
        # Catch any other integrity errors (like unique constraint violations)
        if "duplicate key" in str(e).lower() and "email" in str(e).lower():
            logger.warning(f"Database integrity error for email: {candidate.email}")
            raise EmailAlreadyExistsError(email=candidate.email) from e
        raise

def delete_candidate(db: Session, candidate_id: int):
    """Delete a candidate by ID."""
    candidate = get_candidate(db, candidate_id)
    if not candidate:
        raise CandidateNotFoundError(candidate_id)
    
    db.delete(candidate)
    db.commit()
    logger.info(f"Deleted candidate with ID {candidate_id}")
    return None

def update_candidate(db: Session, candidate_id: int, candidate: CandidateUpdate):
    """Update an existing candidate."""
    db_candidate = get_candidate(db, candidate_id)
    if not db_candidate:
        raise CandidateNotFoundError(candidate_id)
    
    update_data = candidate.model_dump(exclude_unset=True)
    
    # Handle email uniqueness
    if "email" in update_data and update_data["email"] != db_candidate.email:
        existing = get_candidate_by_email(db, update_data["email"])
        if existing:
            logger.warning(f"Attempt to update candidate with duplicate email: {update_data['email']}")
            raise EmailAlreadyExistsError(email=update_data["email"])
    
    for key, value in update_data.items():
        setattr(db_candidate, key, value)
    
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    logger.info(f"Updated candidate with ID {db_candidate.candidate_id}")
    return db_candidate
