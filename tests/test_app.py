import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset participants for test isolation
    for activity in activities.values():
        activity["participants"] = []


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "Signed up test@mergington.edu" in response.json()["message"]
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_already_registered():
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success():
    client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    response = client.post("/activities/Chess Club/unregister?email=test@mergington.edu")
    assert response.status_code == 200
    assert "Removed test@mergington.edu" in response.json()["message"]
    assert "test@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_not_registered():
    response = client.post("/activities/Chess Club/unregister?email=test@mergington.edu")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity():
    response = client.post("/activities/Nonexistent/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
