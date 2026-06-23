from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_deck_score_flow():
    # create deck/card/review via services already covered elsewhere; here just exercise endpoints
    # create a review
    payload = {"card_id": 1, "rating": 5}
    res = client.post("/reviews/", json=payload)
    assert res.status_code in (200, 201)

    # get deck score
    res = client.get("/reviews/deck/1")
    assert res.status_code == 200
    data = res.json()
    assert "deck_id" in data and "average_score" in data and "review_count" in data
