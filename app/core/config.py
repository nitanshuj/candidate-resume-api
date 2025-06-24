# Configuration settings for the application
import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Base settings class."""
    PROJECT_NAME: str = "Candidate & Resume Management API"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/candidate_recruitment")
    
    # CORS settings
    CORS_ORIGINS: list = ["*"]
    
    # Security
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        case_sensitive = True

settings = Settings()
