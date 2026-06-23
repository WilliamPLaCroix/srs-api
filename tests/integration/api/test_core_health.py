import logging

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok():
    res = client.get("/core/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "db": "connected"}


def test_health_logs_info(caplog):
    caplog.set_level(logging.INFO)
    res = client.get("/core/health")
    assert res.status_code == 200
    assert "Health check successful" in caplog.text
