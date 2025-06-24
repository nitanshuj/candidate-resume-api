"""CRUD operations initialization."""
from app.crud.candidate import (
    get_candidate,
    get_candidate_by_email,
    get_candidates,
    create_candidate,
    delete_candidate
)

from app.crud.resume import (
    get_resume,
    get_resumes,
    create_resume,
    delete_resume
)
