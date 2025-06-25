from fastapi import HTTPException, status

class EmailAlreadyExistsError(HTTPException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "Email already registered.",
                "email": email,
                "suggestion": "Please use a different email address or try logging in."
            }
        )

class CandidateNotFoundError(HTTPException):
    def __init__(self, candidate_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Candidate with ID {candidate_id} not found."
        )

class ResumeNotFoundError(HTTPException):
    def __init__(self, resume_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found."
        )

class DatabaseConnectionError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to the database."
        )
