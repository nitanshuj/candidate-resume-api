import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_create_resume_for_nonexistent_candidate():
    response = client.post("/resumes/", json={
        "candidate_id": 9999,
        "title": "Resume Title",
        "file_url": "http://example.com/resume.pdf"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Candidate with ID 9999 not found."

def test_candidate_can_have_multiple_resumes():
    """Test that one candidate can have multiple resumes."""
    # Create a new candidate
    unique_email = f"multi_resume_{uuid.uuid4().hex[:8]}@example.com"
    
    candidate_response = client.post("/candidates/", json={
        "first_name": "Multiple",
        "last_name": "Resumes",
        "email": unique_email,
        "phone": "1234567890"
    })
    
    candidate_id = candidate_response.json()["candidate_id"]
    
    # Create first resume
    resume1_response = client.post("/resumes/", json={
        "candidate_id": candidate_id,
        "title": "Resume One",
        "file_url": "http://example.com/resume1.pdf"
    })
    assert resume1_response.status_code == 201
    
    # Create second resume
    resume2_response = client.post("/resumes/", json={
        "candidate_id": candidate_id,
        "title": "Resume Two",
        "file_url": "http://example.com/resume2.pdf"
    })
    assert resume2_response.status_code == 201
    
    # Verify candidate has multiple resumes
    candidate_details = client.get(f"/candidates/{candidate_id}").json()
    assert "resumes" in candidate_details
    assert len(candidate_details["resumes"]) >= 2

def test_update_resume():
    """Test updating a resume."""
    # First create a candidate
    unique_email = f"resume_update_{uuid.uuid4().hex[:8]}@example.com"
    
    candidate_response = client.post("/candidates/", json={
        "first_name": "Resume",
        "last_name": "Update",
        "email": unique_email,
        "phone": "1234567890"
    })
    assert candidate_response.status_code == 201
    candidate_id = candidate_response.json()["candidate_id"]
    
    # Create a resume for this candidate
    resume_response = client.post("/resumes/", json={
        "candidate_id": candidate_id,
        "title": "Original Resume",
        "file_url": "http://example.com/original.pdf"
    })
    assert resume_response.status_code == 201
    resume_id = resume_response.json()["resume_id"]
    
    # Update the resume
    update_response = client.put(f"/resumes/{resume_id}", json={
        "title": "Updated Resume",
        "file_url": "http://example.com/updated.pdf"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    
    # Verify updates were applied correctly
    assert updated_data["title"] == "Updated Resume"
    assert updated_data["file_url"] == "http://example.com/updated.pdf"
    assert updated_data["resume_id"] == resume_id
    assert updated_data["candidate_id"] == candidate_id
    
    # Confirm by getting the resume
    get_response = client.get(f"/resumes/{resume_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data == updated_data

def test_update_resume_partial():
    """Test updating only some fields of a resume."""
    # First create a candidate
    unique_email = f"resume_partial_{uuid.uuid4().hex[:8]}@example.com"
    
    candidate_response = client.post("/candidates/", json={
        "first_name": "Resume",
        "last_name": "Partial",
        "email": unique_email,
        "phone": "1234567890"
    })
    assert candidate_response.status_code == 201
    candidate_id = candidate_response.json()["candidate_id"]
    
    # Create a resume for this candidate
    resume_response = client.post("/resumes/", json={
        "candidate_id": candidate_id,
        "title": "Original Resume",
        "file_url": "http://example.com/original.pdf"
    })
    assert resume_response.status_code == 201
    resume_id = resume_response.json()["resume_id"]
    original_file_url = resume_response.json()["file_url"]
    
    # Update only the title
    update_response = client.put(f"/resumes/{resume_id}", json={
        "title": "Only Title Updated"
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    
    # Verify only title was updated, file_url remains unchanged
    assert updated_data["title"] == "Only Title Updated"
    assert updated_data["file_url"] == original_file_url
    assert updated_data["resume_id"] == resume_id
    
    # Confirm by getting the resume
    get_response = client.get(f"/resumes/{resume_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data == updated_data

def test_update_nonexistent_resume():
    """Test updating a resume that doesn't exist."""
    nonexistent_id = 99999  # Assuming this ID doesn't exist
    
    response = client.put(f"/resumes/{nonexistent_id}", json={
        "title": "This Won't Work",
        "file_url": "http://example.com/nonexistent.pdf"
    })
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
