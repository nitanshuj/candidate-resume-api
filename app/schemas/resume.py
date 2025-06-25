"""Pydantic schemas for resumes."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
        from_attributes = True  # Updated from orm_mode

class ResumeUpdate(BaseModel):
    title: str | None = None
    file_url: str | None = None
    
    class Config:
        from_attributes = True