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


def create_asset_payload():
    return {"name": "uav1", "sensor_type": "optical"}


def test_asset_crud():
    payload = create_asset_payload()
    resp = client.post("/v1/assets", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    asset_id = data["id"]
    assert data["name"] == payload["name"]

    resp = client.get(f"/v1/assets/{asset_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == asset_id

    resp = client.get("/v1/assets")
    assert resp.status_code == 200
    assert any(a["id"] == asset_id for a in resp.json())

    payload_update = payload | {"name": "updated"}
    resp = client.put(f"/v1/assets/{asset_id}", json=payload_update)
    assert resp.status_code == 200
    assert resp.json()["name"] == "updated"

    resp = client.delete(f"/v1/assets/{asset_id}")
    assert resp.status_code == 200
    resp = client.get(f"/v1/assets/{asset_id}")
    assert resp.status_code == 404
