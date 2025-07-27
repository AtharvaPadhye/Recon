import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.routers import events as events_router

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db():
    events_router.events_db.clear()
    yield
    events_router.events_db.clear()

def create_event_payload():
    return {
        "source_type": "osint",
        "source_id": "test_src",
        "timestamp": "2025-01-01T00:00:00Z",
        "location": {"lat": 1.0, "lon": 2.0},
        "summary": "test"
    }

def test_event_crud():
    payload = create_event_payload()
    # create
    resp = client.post("/v1/events", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    event_id = data["id"]
    for key in payload:
        if key != "location":
            assert data[key] == payload[key]
    assert data["location"] == payload["location"]

    # read
    resp = client.get(f"/v1/events/{event_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == event_id

    # list
    resp = client.get("/v1/events")
    assert resp.status_code == 200
    assert any(e["id"] == event_id for e in resp.json())

    # update
    payload_update = payload | {"summary": "updated"}
    resp = client.put(f"/v1/events/{event_id}", json=payload_update)
    assert resp.status_code == 200
    assert resp.json()["summary"] == "updated"

    # delete
    resp = client.delete(f"/v1/events/{event_id}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "deleted"

    resp = client.get(f"/v1/events/{event_id}")
    assert resp.status_code == 404
