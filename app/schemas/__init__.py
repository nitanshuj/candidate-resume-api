"""Pydantic schemas for candidates and resumes."""
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Resume schemas
class ResumeBase(BaseModel):
    title: str
    file_url: str

class ResumeCreate(ResumeBase):
    candidate_id: int

class Resume(ResumeBase):
    resume_id: int
    candidate_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True

# Candidate schemas
class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    candidate_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    resumes: List[Resume] = []

    class Config:
        orm_mode = True
