# Candidate & Resume Management API

A FastAPI backend for managing candidates and their resumes with a focus on robust data integrity, efficient API design, and production-grade error handling.

## Features
- Complete CRUD operations for both Candidates and Resumes
- PostgreSQL with SQLAlchemy ORM for data persistence and modeling
- Pydantic validation for request/response data
- Proper relational integrity with cascading deletes
- Comprehensive error handling with meaningful error responses
- Modular, production-ready codebase with clear separation of concerns
- Pagination support for listing endpoints
- Unit tests for business logic and constraints

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/candidate-resume-api.git
   cd candidate-resume-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL**
   - Install PostgreSQL if not already installed
     ```bash
     # Ubuntu
     sudo apt-get update && sudo apt-get install postgresql postgresql-contrib
     
     # macOS with Homebrew
     brew install postgresql
     
     # Windows
     # Download installer from https://www.postgresql.org/download/windows/
     ```
   
   - Create a database for the application
     ```bash
     # Start PostgreSQL service if needed
     # Linux: sudo service postgresql start
     # macOS: brew services start postgresql
     
     # Create database
     psql -U postgres -c "CREATE DATABASE candidate_resume_db;"
     
     # Optional: Create a dedicated user
     psql -U postgres -c "CREATE USER candidate_user WITH PASSWORD 'password';"
     psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE candidate_resume_db TO candidate_user;"
     ```

4. **Configure environment**
   - Create a `.env` file in the project root:
     ```
     DATABASE_URL=postgresql://postgres:postgres@localhost:5432/candidate_resume_db
     LOG_LEVEL=INFO
     ```
   - Adjust the connection string according to your PostgreSQL setup

5. **Create database tables**
   ```bash
   python -m scripts.create_tables
   ```

6. **Start the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Usage Examples

### Candidate Operations

#### Create a Candidate
```bash
curl -X POST "http://localhost:8000/candidates/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "1234567890"
  }'
```
Response (201 Created):
```json
{
  "candidate_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "created_at": "2025-06-24T14:30:00",
  "updated_at": "2025-06-24T14:30:00",
  "resumes": []
}
```

#### Get All Candidates (with pagination)
```bash
curl -X GET "http://localhost:8000/candidates/?skip=0&limit=10"
```

#### Get a Specific Candidate
```bash
curl -X GET "http://localhost:8000/candidates/1"
```

#### Update a Candidate
```bash
curl -X PUT "http://localhost:8000/candidates/1" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Johnny",
    "phone": "9876543210"
  }'
```

#### Delete a Candidate (cascades to resumes)
```bash
curl -X DELETE "http://localhost:8000/candidates/1"
```

### Resume Operations

#### Create a Resume
```bash
curl -X POST "http://localhost:8000/resumes/" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 1,
    "title": "Software Engineer Resume",
    "file_url": "http://example.com/resume.pdf"
  }'
```
Response (201 Created):
```json
{
  "resume_id": 1,
  "candidate_id": 1,
  "title": "Software Engineer Resume",
  "file_url": "http://example.com/resume.pdf",
  "uploaded_at": "2025-06-24T14:35:00"
}
```

#### Get All Resumes
```bash
curl -X GET "http://localhost:8000/resumes/?skip=0&limit=10"
```

#### Get a Specific Resume
```bash
curl -X GET "http://localhost:8000/resumes/1"
```

#### Update a Resume
```bash
curl -X PUT "http://localhost:8000/resumes/1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Software Engineer Resume",
    "file_url": "http://example.com/updated-resume.pdf"
  }'
```

#### Delete a Resume
```bash
curl -X DELETE "http://localhost:8000/resumes/1"
```

## Error Handling Examples

### Duplicate Email
```bash
# Create first candidate
curl -X POST "http://localhost:8000/candidates/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "duplicate@example.com",
    "phone": "1234567890"
  }'

# Try to create another with same email
curl -X POST "http://localhost:8000/candidates/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "duplicate@example.com",
    "phone": "9876543210"
  }'
```
Error Response (409 Conflict):
```json
{
  "message": "Email already registered.",
  "email": "duplicate@example.com"
}
```

### Resume for Non-existent Candidate
```bash
curl -X POST "http://localhost:8000/resumes/" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_id": 999,
    "title": "Invalid Resume",
    "file_url": "http://example.com/invalid.pdf"
  }'
```
Error Response (404 Not Found):
```json
{
  "detail": "Candidate with ID 999 not found."
}
```

## Testing

Run the full test suite:
```bash
python -m pytest
```

Run a specific test file:
```bash
python -m pytest tests/test_candidates.py -v
```

Run tests with coverage report:
```bash
python -m pytest --cov=app tests/
```

## Project Structure

```
candidate-resume-api/
├── app/                    # Main application package
│   ├── core/               # Core functionality
│   │   ├── config.py       # Configuration settings
│   │   ├── database.py     # Database connection
│   │   ├── exceptions.py   # Custom exceptions
│   │   └── logger.py       # Logging configuration
│   ├── crud/               # CRUD operations
│   │   ├── base.py         # Base CRUD operations
│   │   ├── candidate.py    # Candidate-specific operations
│   │   └── resume.py       # Resume-specific operations
│   ├── models/             # SQLAlchemy models
│   │   ├── base.py         # Base model class
│   │   ├── candidate.py    # Candidate model
│   │   └── resume.py       # Resume model
│   ├── routers/            # API routes
│   │   ├── candidates.py   # Candidate endpoints
│   │   └── resumes.py      # Resume endpoints
│   ├── schemas/            # Pydantic schemas
│   │   ├── candidate.py    # Candidate schemas
│   │   └── resume.py       # Resume schemas
│   └── main.py             # FastAPI application
├── logs/                   # Log files
├── scripts/                # Utility scripts
│   ├── create_tables.py    # Database initialization
│   └── seed_data.py        # Sample data generation
├── tests/                  # Test suite
│   ├── test_candidates.py  # Tests for candidate operations
│   └── test_resumes.py     # Tests for resume operations
├── .env                    # Environment variables
├── .gitignore              # Git ignore file
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## Architecture

This project follows a layered architecture designed for maintainability, testability, and separation of concerns:

1. **API Layer** (routers): Handles HTTP requests and responses, input validation, and status codes.

2. **Service Layer** (crud): Implements business logic and operations on data models.

3. **Data Layer** (models): Defines the database schema and ORM models.

4. **Schema Layer** (schemas): Manages data validation, serialization, and deserialization.

5. **Core Components**:
   - **Database**: Connection management and session handling
   - **Exceptions**: Custom exception classes for specific error cases
   - **Logger**: Structured logging facility
   - **Config**: Configuration management

## Key Design Decisions

- **SQLAlchemy ORM**: For type-safe database operations and migrations
- **Pydantic Models**: For request/response validation and documentation
- **Custom Exceptions**: For clear and consistent error handling
- **Modular Structure**: For maintainability and separation of concerns
- **Repository Pattern**: For abstracting database operations
- **Comprehensive Testing**: To ensure business rules are enforced

## API Documentation

### Swagger UI (Interactive Documentation)

The API comes with built-in interactive documentation powered by Swagger UI:

1. Start the application server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Access the Swagger UI:
   - Open your browser and navigate to http://localhost:8000/docs
   - You can explore all endpoints, execute requests, and view response models

### Alternative Documentation

- ReDoc (alternative documentation view): http://localhost:8000/redoc
- OpenAPI Specification: http://localhost:8000/openapi.json

### Swagger YAML File

A `swagger.yaml` file is also provided in the project root, which can be imported into tools like Postman, SwaggerHub, or other API development tools.

To generate an updated `swagger.yaml` file from a running server, use:
```bash
python -m scripts.swagger_utils --export
```
