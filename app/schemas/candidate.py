"""Pydantic schemas for candidates."""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional
from datetime import datetime

# Import Resume schema for relationship
from app.schemas.resume import Resume

class CandidateBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str | None = Field(None, max_length=20)
    
    @validator('email')
    def email_must_be_lowercase(cls, v):
        """Normalize email to lowercase to prevent case-sensitivity duplicates."""
        return v.lower() if v else v

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    candidate_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    resumes: List[Resume] = []

    class Config:
        from_attributes = True  # Updated from orm_mode

class CandidateUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    
    class Config:
        from_attributes = True