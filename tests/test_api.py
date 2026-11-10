from fastapi.testclient import TestClient
from app.main import app

def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_empty_chat_is_rejected():
    with TestClient(app) as client:
        response = client.post("/api/v1/chat", json={"message":""})
    assert response.status_code == 422
