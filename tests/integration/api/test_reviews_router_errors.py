from fastapi.testclient import TestClient

from app.main import app
from app.modules.reviews import router as reviews_router

client = TestClient(app)


def _patch_and_call(patcher, path, method="get", json=None):
    original = reviews_router.get_review_service
    reviews_router.get_review_service = patcher
    try:
        if method == "get":
            return client.get(path)
        if method == "post":
            return client.post(path, json=json)
    finally:
        reviews_router.get_review_service = original


def test_create_review_500_on_service_error():
    def bad_service(session):
        class S:
            def create_review(self, card_id, rating):
                raise RuntimeError("boom")

        return S()

    res = _patch_and_call(bad_service, "/reviews/", method="post", json={"card_id": 1, "rating": 5})
    assert res is not None
    assert res.status_code == 500


def test_get_deck_score_500_on_service_error():
    def bad_service(session):
        class S:
            def compute_deck_score(self, deck_id):
                raise RuntimeError("boom")

        return S()

    res = _patch_and_call(bad_service, "/reviews/deck/1")
    assert res is not None
    assert res.status_code == 500


# ValueError -> HTTP mappings


def test_create_review_400_on_validation_error():
    def bad_service(session):
        class S:
            def create_review(self, card_id, rating):
                raise ValueError("Rating must be 1–5")

        return S()

    res = _patch_and_call(
        bad_service,
        "/reviews/",
        method="post",
        json={"card_id": 1, "rating": 999},
    )
    assert res is not None
    assert res.status_code == 400
    assert res.json().get("detail") == "Rating must be 1–5"
