from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_get_full_delete_flow():
    # create
    payload = {"name": "Languages"}
    res = client.post("/decks/", json=payload)
    assert res.status_code == 200
    deck = res.json()
    deck_id = deck["id"]

    # get
    res = client.get(f"/decks/{deck_id}")
    assert res.status_code == 200

    # get full (no cards yet)
    res = client.get(f"/decks/{deck_id}/full")
    assert res.status_code == 200
    assert res.json()["id"] == deck_id
    assert res.json()["cards"] == []

    # delete
    res = client.delete(f"/decks/{deck_id}")
    assert res.status_code == 200

    # verify gone
    res = client.get(f"/decks/{deck_id}")
    assert res.status_code == 404


def test_get_deck_not_found():
    res = client.get("/decks/99999")
    assert res.status_code == 404
