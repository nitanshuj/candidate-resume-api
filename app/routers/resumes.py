from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Resume, status_code=status.HTTP_201_CREATED)
def create_resume(resume: schemas.ResumeCreate, db: Session = Depends(get_db)):
    return crud.create_resume(db, resume)

@router.get("/", response_model=List[schemas.Resume])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_resumes(db, skip=skip, limit=limit)

@router.get("/{resume_id}", response_model=schemas.Resume)
def read_resume(resume_id: int, db: Session = Depends(get_db)):
    db_resume = crud.get_resume(db, resume_id)
    if db_resume is None:
        raise HTTPException(status_code=404, detail="Resume not found.")
    return db_resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    crud.delete_resume(db, resume_id)
    return
