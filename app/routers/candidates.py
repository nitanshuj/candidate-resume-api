from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.crud.candidate import get_candidate, get_candidates, create_candidate, delete_candidate, update_candidate
from app.core.database import get_db
from app.core.exceptions import CandidateNotFoundError, EmailAlreadyExistsError
from app.core.logger import logger

router = APIRouter()

@router.post("/", response_model=schemas.Candidate, status_code=status.HTTP_201_CREATED)
def create_candidate_endpoint(candidate: schemas.CandidateCreate, 
                     db: Session = Depends(get_db)):
    """Create a new candidate."""
    try:
        logger.info(f"Creating new candidate with email: {candidate.email}")
        return create_candidate(db=db, candidate=candidate)
    except EmailAlreadyExistsError as e:
        # Let the global exception handler deal with this
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating candidate: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred."
        ) from e

@router.get("/", response_model=List[schemas.Candidate])
def read_candidates(skip: int = 0, 
                    limit: int = 100, 
                    db: Session = Depends(get_db)):
    """Get all candidates with pagination."""
    candidates = get_candidates(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(candidates)} candidates")
    return candidates

@router.get("/{candidate_id}", response_model=schemas.Candidate)
def read_candidate(candidate_id: int, 
                   db: Session = Depends(get_db)):
    """Get a specific candidate by ID."""
    logger.info(f"Fetching candidate with ID: {candidate_id}")
    db_candidate = get_candidate(db, candidate_id)
    if db_candidate is None:
        raise CandidateNotFoundError(candidate_id)
    return db_candidate

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate_endpoint(candidate_id: int, 
                     db: Session = Depends(get_db)):
    """Delete a candidate by ID."""
    logger.info(f"Deleting candidate with ID: {candidate_id}")
    delete_candidate(db, candidate_id)
    return

@router.put("/{candidate_id}", response_model=schemas.Candidate)
def update_candidate_endpoint(candidate_id: int, candidate: schemas.CandidateUpdate, db: Session = Depends(get_db)):
    """Update candidate details."""
    try:
        logger.info(f"Updating candidate ID: {candidate_id}")
        return update_candidate(db, candidate_id, candidate)
    except CandidateNotFoundError:
        raise
    except EmailAlreadyExistsError as e:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating candidate {candidate_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the candidate."
        ) from e
