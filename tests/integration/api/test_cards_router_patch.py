from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_patch_card_success_flow():
    # create a card
    payload = {"front": "Old?", "back": "Old answer", "deck_id": 1}
    res = client.post("/cards/", json=payload)
    assert res.status_code == 200
    card = res.json()
    card_id = card["id"]

    # patch it
    patch_payload = {"front": "New?"}
    res = client.patch(f"/cards/{card_id}", json=patch_payload)
    assert res.status_code == 200
    updated = res.json()
    assert updated["front"] == "New?"
    assert updated["id"] == card_id


def test_patch_card_no_fields_ok_returns_400():
    # create another card
    payload = {"front": "F", "back": "B", "deck_id": 1}
    res = client.post("/cards/", json=payload)
    assert res.status_code == 200
    card_id = res.json()["id"]

    # patch with no fields
    res = client.patch(f"/cards/{card_id}", json={})
    assert res.status_code == 400


def test_patch_card_not_found_returns_404():
    res = client.patch("/cards/999999", json={"front": "X"})
    assert res.status_code == 404
