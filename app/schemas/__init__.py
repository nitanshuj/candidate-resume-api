"""Schema re-exports for easier imports."""
# Re-export all schemas to maintain compatibility
from app.schemas.candidate import CandidateBase, CandidateCreate, Candidate, CandidateUpdate
from app.schemas.resume import ResumeBase, ResumeCreate, Resume, ResumeUpdate

__all__ = [
    'CandidateBase', 
    'CandidateCreate', 
    'Candidate', 
    'CandidateUpdate',
    'ResumeBase', 
    'ResumeCreate', 
    'Resume', 
    'ResumeUpdate'
]

