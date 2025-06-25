from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers import candidates, resumes
from app.core.logger import logger
from app.core.exceptions import (
    EmailAlreadyExistsError,
    CandidateNotFoundError,
    ResumeNotFoundError,
    DatabaseConnectionError
)

# Create FastAPI app
app = FastAPI(
    title="Candidate & Resume Management API",
    description="A FastAPI backend for managing candidates and their resumes with a focus on robust data integrity, efficient API design, and production-grade error handling.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Candidates", "description": "Operations related to candidate management"},
        {"name": "Resumes", "description": "Operations related to resume management"},
        {"name": "Health", "description": "API health check endpoints"},
        {"name": "Root", "description": "API information endpoint"},
    ],
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add global exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(EmailAlreadyExistsError)
async def email_exists_exception_handler(request: Request, exc: EmailAlreadyExistsError):
    logger.warning(f"Duplicate email attempt: {exc.detail.get('email')}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )

# Include routers
app.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
app.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])

# Add health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint that provides basic API information.
    """
    return {
        "message": "Welcome to Candidate Resume API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "candidates": "/candidates",
            "resumes": "/resumes"
        }
    }
