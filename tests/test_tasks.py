import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import memory_db as database

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
        "summary": "event"
    }
    return client.post("/v1/events", json=payload).json()["id"]

def create_case(event_id):
    payload = {
        "title": "case",
        "location": {"lat": 0, "lon": 0},
        "initial_event_id": event_id
    }
    return client.post("/v1/cases", json=payload).json()["id"]

def create_task_payload(case_id):
    return {
        "case_id": case_id,
        "sensor_types": ["optical"],
        "urgency": "high",
        "preferred_assets": ["uav"]
    }

def test_task_crud():
    event_id = create_event()
    case_id = create_case(event_id)
    payload = create_task_payload(case_id)

    # create
    resp = client.post("/v1/task_recon", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    task_id = data["id"]
    assert data["case_id"] == case_id

    # read
    resp = client.get(f"/v1/task_recon/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == task_id

    # list
    resp = client.get("/v1/task_recon")
    assert resp.status_code == 200
    assert any(t["id"] == task_id for t in resp.json())

    # update
    payload_update = payload | {"urgency": "low"}
    resp = client.put(f"/v1/task_recon/{task_id}", json=payload_update)
    assert resp.status_code == 200
    assert resp.json()["urgency"] == "low"

    # delete
    resp = client.delete(f"/v1/task_recon/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["detail"] == "deleted"

    resp = client.get(f"/v1/task_recon/{task_id}")
    assert resp.status_code == 404
