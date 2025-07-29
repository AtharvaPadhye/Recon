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


def create_event():
    payload = {
        "source_type": "osint",
        "source_id": "src",
        "timestamp": "2025-01-01T00:00:00Z",
        "location": {"lat": 0, "lon": 0},
        "summary": "event",
    }
    resp = client.post("/v1/events", json=payload)
    return resp.json()["id"]


def create_case(event_id):
    payload = {
        "title": "case",
        "location": {"lat": 0, "lon": 0},
        "initial_event_id": event_id,
    }
    resp = client.post("/v1/cases", json=payload)
    return resp.json()["id"]


def test_entities_list_and_get():
    event_id = create_event()
    case_id = create_case(event_id)

    resp = client.get("/entities/Case")
    assert resp.status_code == 200
    assert any(c["id"] == case_id for c in resp.json())

    resp = client.get(f"/entities/Case/{case_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == case_id
