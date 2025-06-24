"""Script to create database tables."""
from app.core.database import Base, engine
from app.core.logger import logger

# Import all models to register them with Base
from app.models.candidate import Candidate
from app.models.resume import Resume

def create_tables():
    """Create all database tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully!")
        print("Tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        print(f"Error creating tables: {str(e)}")

if __name__ == "__main__":
    create_tables()
