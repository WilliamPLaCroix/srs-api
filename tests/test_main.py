from fastapi.testclient import TestClient
from app.main import app
from app.db.base import Base
from app.db.engine import engine

client = TestClient(app)
Base.metadata.create_all(bind=engine)

def test_app_starts():
    response = client.get("/")
    assert response.status_code == 200

def test_cards_endpoint_exists():
    response = client.get("/cards")
    assert response.status_code != 404

def test_create_card_api_flow():
    payload = {
        "front": "Q",
        "back": "A",
        "deck_id": 1
    }

    response = client.post("/cards", json=payload)

    assert response.status_code in (200, 201)
    data = response.json()
    assert "id" in data