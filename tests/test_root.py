from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_serves_index():
    resp = client.get('/')
    assert resp.status_code == 200
    assert '<!DOCTYPE html>' in resp.text
