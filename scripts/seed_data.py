"""Script to seed the database with sample data."""
from app.core.database import SessionLocal
from app.core.logger import logger
from app.models.candidate import Candidate
from app.models.resume import Resume

def seed_data():
    """Seed the database with sample data."""
    try:
        db = SessionLocal()
        
        # Check if data already exists
        if db.query(Candidate).count() > 0:
            logger.warning("Database already contains data. Seeding skipped.")
            print("Database already contains data. Seeding skipped.")
            return
        
        # Create sample candidates
        candidates = [
            Candidate(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                phone="1234567890",
            ),
            Candidate(
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                phone="9876543210",
            ),
            Candidate(
                first_name="Bob",
                last_name="Johnson",
                email="bob.johnson@example.com",
                phone="5551234567",
            ),
        ]
        
        db.add_all(candidates)
        db.commit()
        
        # Create sample resumes
        resumes = [
            Resume(
                candidate_id=1,
                title="Software Developer Resume",
                file_url="http://example.com/resumes/johndoe_dev.pdf",
            ),
            Resume(
                candidate_id=1,
                title="Project Manager Resume",
                file_url="http://example.com/resumes/johndoe_pm.pdf",
            ),
            Resume(
                candidate_id=2,
                title="UX Designer Resume",
                file_url="http://example.com/resumes/janesmith_ux.pdf",
            ),
            Resume(
                candidate_id=3,
                title="Data Scientist Resume",
                file_url="http://example.com/resumes/bobjohnson_ds.pdf",
            ),
        ]
        
        db.add_all(resumes)
        db.commit()
        
        logger.info("Database seeded successfully!")
        print("Database seeded successfully!")
        
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
