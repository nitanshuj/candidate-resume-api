import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.core.logger import logger

# Load environment variables
load_dotenv()

# Create database engine and session
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/Candidate_Recruitment"
    logger.warning("DATABASE_URL not found in environment variables. Using default.")

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    # We'll import the exception later to avoid circular imports
    # raise DatabaseConnectionError()

def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.debug("Database session yielded successfully")
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed")
