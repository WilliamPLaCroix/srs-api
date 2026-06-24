from fastapi.testclient import TestClient

from app.main import app


def test_create_and_get_card_score_flow():
    with TestClient(app) as client:
        # create deck and card
        deck = client.post("/decks/", json={"name": "D"}).json()
        card = client.post(
            "/cards/", json={"front": "Q", "back": "A", "deck_id": deck["id"]}
        ).json()

        # no reviews yet
        res = client.get(f"/reviews/card/{card['id']}")
        assert res.status_code == 200
        assert res.json()["average_score"] == 0.0

        # create reviews
        client.post("/reviews/", json={"card_id": card["id"], "rating": 5})
        client.post("/reviews/", json={"card_id": card["id"], "rating": 3})

        res = client.get(f"/reviews/card/{card['id']}")
        assert res.status_code == 200
        data = res.json()
        assert data["review_count"] == 2
        assert data["average_score"] == 4.0
