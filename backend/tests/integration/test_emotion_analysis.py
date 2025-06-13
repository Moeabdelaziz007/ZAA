import pytest
from fastapi.testclient import TestClient
from ..core.auth import create_access_token
from ..models.user import User
from ..main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User"
    )

@pytest.fixture
def test_token(test_user):
    return create_access_token({"sub": test_user.username})

def test_emotion_analysis_flow(test_token):
    # Test text analysis
    response = client.post(
        "/api/emotions/analyze",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"text": "I am very happy today!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "emotion" in data
    assert "confidence" in data
    assert data["emotion"] == "happy"

    # Test weekly analysis
    response = client.get(
        "/api/emotions/weekly",
        headers={"Authorization": f"Bearer {test_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)

def test_emotion_analysis_validation(test_token):
    # Test empty text
    response = client.post(
        "/api/emotions/analyze",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"text": ""}
    )
    assert response.status_code == 400
    assert "text" in response.json()["detail"]

    # Test very long text
    long_text = "a" * 1001
    response = client.post(
        "/api/emotions/analyze",
        headers={"Authorization": f"Bearer {test_token}"},
        json={"text": long_text}
    )
    assert response.status_code == 400
    assert "text" in response.json()["detail"] 
