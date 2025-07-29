import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import database

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    database.clear_db()
    yield
    database.clear_db()


def test_process_event_creates_case():
    event_payload = {
        "source_type": "osint",
        "source_id": "src",
        "timestamp": "2025-01-01T00:00:00Z",
        "location": {"lat": 0, "lon": 0},
        "summary": "troop movement detected",
    }
    event_id = client.post("/v1/events", json=event_payload).json()["id"]
    resp = client.post(f"/v1/events/{event_id}/process")
    assert resp.status_code == 200
    data = resp.json()
    assert data["initial_event_id"] == event_id
