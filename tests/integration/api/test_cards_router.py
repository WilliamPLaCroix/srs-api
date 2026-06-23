from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_get_list_delete_endpoints():
    # create
    payload = {"front": "What is FastAPI?", "back": "A Python web framework", "deck_id": 1}
    res = client.post("/cards/", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["front"] == "What is FastAPI?"
    card_id = data["id"]

    # get
    res = client.get(f"/cards/{card_id}")
    assert res.status_code == 200
    assert res.json()["id"] == card_id

    # list by deck
    res = client.get("/cards/deck/1")
    assert res.status_code == 200
    items = res.json()
    assert any(i["id"] == card_id for i in items)

    # delete
    res = client.delete(f"/cards/{card_id}")
    assert res.status_code == 200
    assert res.json().get("detail") == "Card deleted"

    # ensure gone
    res = client.get(f"/cards/{card_id}")
    assert res.status_code == 404


def test_get_card_not_found():
    res = client.get("/cards/999999")
    assert res.status_code == 404
