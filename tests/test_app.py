import pytest
from fastapi.testclient import TestClient

# Arrange: Setup test client fixture
@pytest.fixture
def client():
    from src.app import app
    return TestClient(app)

# Arrange: Sample activity and email
ACTIVITY = "Chess Club"
EMAIL = "testuser@mergington.edu"


def test_get_root_redirect(client):
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200 or response.status_code == 307
    assert "html" in response.text


def test_get_activities(client):
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert ACTIVITY in response.json()


def test_signup_success(client):
    # Arrange
    signup_url = f"/activities/{ACTIVITY}/signup?email={EMAIL}"
    # Act
    response = client.post(signup_url)
    # Assert
    assert response.status_code == 200
    assert f"Signed up {EMAIL}" in response.json()["message"]


def test_signup_duplicate(client):
    # Arrange
    signup_url = f"/activities/{ACTIVITY}/signup?email={EMAIL}"
    # Act
    response = client.post(signup_url)
    response_dup = client.post(signup_url)
    # Assert
    assert response_dup.status_code == 400
    assert "already signed up" in response_dup.json()["detail"]


def test_signup_activity_not_found(client):
    # Arrange
    signup_url = "/activities/Nonexistent/signup?email=someone@mergington.edu"
    # Act
    response = client.post(signup_url)
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success(client):
    # Arrange
    signup_url = f"/activities/{ACTIVITY}/signup?email={EMAIL}"
    unregister_url = f"/activities/{ACTIVITY}/unregister?email={EMAIL}"
    client.post(signup_url)  # Ensure user is signed up
    # Act
    response = client.delete(unregister_url)
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {EMAIL}" in response.json()["message"]


def test_unregister_not_signed_up(client):
    # Arrange
    unregister_url = f"/activities/{ACTIVITY}/unregister?email=notregistered@mergington.edu"
    # Act
    response = client.delete(unregister_url)
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_activity_not_found(client):
    # Arrange
    unregister_url = "/activities/Nonexistent/unregister?email=someone@mergington.edu"
    # Act
    response = client.delete(unregister_url)
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
