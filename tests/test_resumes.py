import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_resume_for_nonexistent_candidate():
    response = client.post("/resumes/", json={
        "candidate_id": 9999,
        "title": "Resume Title",
        "file_url": "http://example.com/resume.pdf"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate with ID 9999 not found."
