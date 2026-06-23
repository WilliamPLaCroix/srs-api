from types import SimpleNamespace

import pytest

from app.modules.reviews.services import ReviewService


class FakeRepo:
    def create(self, card_id, rating):
        return SimpleNamespace(id=1, card_id=card_id, rating=rating)

    def get_by_deck(self, deck_id):
        return [SimpleNamespace(rating=5), SimpleNamespace(rating=3)]

    def delete_by_deck(self, deck_id):
        return {"deleted_count": 1}


def test_create_review_validation_raises():
    svc = ReviewService(FakeRepo())
    with pytest.raises(ValueError):
        svc.create_review(1, 999)


def test_create_review_success():
    svc = ReviewService(FakeRepo())
    r = svc.create_review(1, 4)
    assert r.id == 1


def test_create_review_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def create(self, card_id, rating):
            raise RuntimeError("db error")

    svc = ReviewService(BadRepo())
    with pytest.raises(RuntimeError):
        svc.create_review(1, 4)


def test_compute_deck_score_no_reviews_returns_zero():
    class EmptyRepo(FakeRepo):
        def get_by_deck(self, deck_id):
            return []

    svc = ReviewService(EmptyRepo())
    res = svc.compute_deck_score(1)
    assert res["average_score"] == 0.0
    assert res["review_count"] == 0


def test_compute_deck_score_success():
    svc = ReviewService(FakeRepo())
    res = svc.compute_deck_score(1)
    assert res["average_score"] == 4.0
    assert res["review_count"] == 2


def test_compute_deck_score_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def get_by_deck(self, deck_id):
            raise RuntimeError("query failed")

    svc = ReviewService(BadRepo())
    with pytest.raises(RuntimeError):
        svc.compute_deck_score(1)


def test_delete_deck_reviews_success():
    svc = ReviewService(FakeRepo())
    res = svc.delete_deck_reviews(1)
    assert res["deleted_count"] == 1


def test_delete_deck_reviews_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def delete_by_deck(self, deck_id):
            raise RuntimeError("delete failed")

    svc = ReviewService(BadRepo())
    with pytest.raises(RuntimeError):
        svc.delete_deck_reviews(1)
