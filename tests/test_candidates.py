import pytest
from fastapi.testclient import TestClient
from my_candidate_resume_api.app.main import app

client = TestClient(app)

def test_create_candidate():
    response = client.post("/candidates/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "phone": "1234567890"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"

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
    assert response.json()["detail"] == "Email already registered."
