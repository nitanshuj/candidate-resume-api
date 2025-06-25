import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_candidate():
    import uuid
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    
    response = client.post("/candidates/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": unique_email,
        "phone": "1234567890"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == unique_email

def test_duplicate_email():
    client.post("/candidates/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "duplicate@example.com",
        "phone": "1234567890"
    })
    response = client.post("/candidates/", json={
        "first_name": "Test2",
        "last_name": "User2",
        "email": "duplicate@example.com",
        "phone": "0987654321"
    })
    assert response.status_code == 409
    response_data = response.json()
    assert "message" in response_data
    assert response_data["message"] == "Email already registered."
    assert "email" in response_data
    assert response_data["email"] == "duplicate@example.com"

def test_cascade_delete():
    """Test that deleting a candidate also deletes all their resumes."""
    # Create a candidate
    import uuid
    unique_email = f"cascade_{uuid.uuid4().hex[:8]}@example.com"
    
    candidate_response = client.post("/candidates/", json={
        "first_name": "Cascade",
        "last_name": "Delete",
        "email": unique_email,
        "phone": "1234567890"
    })
    
    candidate_id = candidate_response.json()["candidate_id"]
    
    # Create a resume for this candidate
    resume_response = client.post("/resumes/", json={
        "candidate_id": candidate_id,
        "title": "Will Be Deleted",
        "file_url": "http://example.com/delete.pdf"
    })
    
    resume_id = resume_response.json()["resume_id"]
    
    # Delete the candidate
    delete_response = client.delete(f"/candidates/{candidate_id}")
    assert delete_response.status_code == 204
    
    # Check that the candidate is gone
    get_candidate = client.get(f"/candidates/{candidate_id}")
    assert get_candidate.status_code == 404
    
    # Check that the resume is also gone
    get_resume = client.get(f"/resumes/{resume_id}")
    assert get_resume.status_code == 404

def test_update_candidate():
    """Test updating candidate details."""
    # Create a new candidate
    import uuid
    unique_email = f"update_candidate_{uuid.uuid4().hex[:8]}@example.com"
    
    create_response = client.post("/candidates/", json={
        "first_name": "Before",
        "last_name": "Update",
        "email": unique_email,
        "phone": "1234567890"
    })
    assert create_response.status_code == 201
    candidate_id = create_response.json()["candidate_id"]
    
    # Update the candidate
    new_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"
    update_response = client.put(f"/candidates/{candidate_id}", json={
        "first_name": "After",
        "email": new_email,
        # Not updating last_name or phone
    })
    assert update_response.status_code == 200
    updated_data = update_response.json()
    
    # Verify updates were applied correctly
    assert updated_data["first_name"] == "After"
    assert updated_data["last_name"] == "Update"  # Not changed
    assert updated_data["email"] == new_email
    assert updated_data["phone"] == "1234567890"  # Not changed
    assert updated_data["candidate_id"] == candidate_id
    
    # Confirm by getting the candidate
    get_response = client.get(f"/candidates/{candidate_id}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data == updated_data

def test_update_candidate_nonexistent():
    """Test updating a candidate that doesn't exist."""
    response = client.put("/candidates/99999", json={
        "first_name": "Nonexistent"
    })
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_candidate_duplicate_email():
    """Test updating a candidate with an email that already exists."""
    # Create two candidates
    import uuid
    email1 = f"duplicate_update1_{uuid.uuid4().hex[:8]}@example.com"
    email2 = f"duplicate_update2_{uuid.uuid4().hex[:8]}@example.com"
    
    # First candidate
    response1 = client.post("/candidates/", json={
        "first_name": "First",
        "last_name": "Candidate",
        "email": email1
    })
    
    # Second candidate
    response2 = client.post("/candidates/", json={
        "first_name": "Second",
        "last_name": "Candidate",
        "email": email2
    })
    
    # Try to update second candidate with first candidate's email
    candidate2_id = response2.json()["candidate_id"]
    update_response = client.put(f"/candidates/{candidate2_id}", json={
        "email": email1
    })
    
    # Should fail with 409 Conflict
    assert update_response.status_code == 409
    response_data = update_response.json()
    assert "message" in response_data
    assert response_data["message"] == "Email already registered."
