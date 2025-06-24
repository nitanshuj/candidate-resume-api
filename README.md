# Candidate & Resume Management API

A FastAPI backend for managing candidates and their resumes using PostgreSQL and SQLAlchemy ORM.

## Features
- Candidate and Resume CRUD
- PostgreSQL with SQLAlchemy ORM
- Pydantic validation
- Cascade delete resumes on candidate removal
- Graceful error handling
- Modular, production-ready code

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Edit `.env` for your PostgreSQL credentials
4. **Run migrations**
   ```bash
   # Use Alembic or run the following in Python shell:
   from app.database import Base, engine
   Base.metadata.create_all(bind=engine)
   ```
5. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```

## Example API Calls

### Create Candidate
```bash
curl -X POST "http://localhost:8000/candidates/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john@example.com", "phone": "1234567890"}'
```

### Create Resume
```bash
curl -X POST "http://localhost:8000/resumes/" -H "Content-Type: application/json" -d '{"candidate_id": 1, "title": "Software Engineer", "file_url": "http://example.com/resume.pdf"}'
```

### Delete Candidate (cascade deletes resumes)
```bash
curl -X DELETE "http://localhost:8000/candidates/1"
```

## Testing
```bash
pytest
```
