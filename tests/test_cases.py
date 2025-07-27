import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.routers import cases as cases_router, events as events_router

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    cases_router.cases_db.clear()
    events_router.events_db.clear()
    yield
    cases_router.cases_db.clear()
    events_router.events_db.clear()

def create_event():
    payload = {
        "source_type": "osint",
        "source_id": "src",
        "timestamp": "2025-01-01T00:00:00Z",
        "location": {"lat": 0, "lon": 0},
        "summary": "event"
    }
    resp = client.post("/v1/events", json=payload)
    return resp.json()["id"]

def create_case_payload(event_id):
    return {
        "title": "case",
        "location": {"lat": 0, "lon": 0},
        "initial_event_id": event_id
    }

def test_case_crud():
    event_id = create_event()
    payload = create_case_payload(event_id)
    # create
    resp = client.post("/v1/cases", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    case_id = data["id"]
    assert data["title"] == payload["title"]

    # read
    resp = client.get(f"/v1/cases/{case_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == case_id

    # list
    resp = client.get("/v1/cases")
    assert resp.status_code == 200
    assert any(c["id"] == case_id for c in resp.json())

    # update
    payload_update = payload | {"title": "updated"}
    resp = client.put(f"/v1/cases/{case_id}", json=payload_update)
    assert resp.status_code == 200
    assert resp.json()["title"] == "updated"

    # delete
    resp = client.delete(f"/v1/cases/{case_id}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "deleted"

    resp = client.get(f"/v1/cases/{case_id}")
    assert resp.status_code == 404
