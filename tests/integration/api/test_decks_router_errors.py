from fastapi.testclient import TestClient

from app.main import app
from app.modules.decks import router as decks_router

client = TestClient(app)


def _patch_and_call(patcher, path, method="get", json=None):
    original = decks_router.get_deck_service
    decks_router.get_deck_service = patcher
    try:
        if method == "get":
            return client.get(path)
        if method == "post":
            return client.post(path, json=json)
        if method == "delete":
            return client.delete(path)
    finally:
        decks_router.get_deck_service = original


def test_create_deck_500_on_service_error():
    def bad_service(session):
        class S:
            def create_deck(self, name):
                raise RuntimeError("boom")

        return S()

    res = _patch_and_call(bad_service, "/decks/", method="post", json={"name": "X"})
    assert res is not None
    assert res.status_code == 500


def test_get_deck_500_on_service_error():
    def bad_service(session):
        class S:
            def get_deck(self, deck_id):
                raise RuntimeError("boom")

        return S()

    res = _patch_and_call(bad_service, "/decks/1")
    assert res is not None
    assert res.status_code == 500


def test_get_deck_full_500_on_service_error():
    def bad_service(session):
        class S:
            def get_deck_with_cards(self, deck_id):
                raise RuntimeError("boom")

        return S()

    res = _patch_and_call(bad_service, "/decks/1/full")
    assert res is not None
    assert res.status_code == 500


def test_delete_deck_500_on_service_error():
    def bad_service(session):
        class S:
            def delete_deck(self, deck_id):
                raise RuntimeError("boom")

        return S()

    res = _patch_and_call(bad_service, "/decks/1", method="delete")
    assert res is not None
    assert res.status_code == 500


# --- New tests for ValueError -> HTTP mappings ---


def test_create_deck_400_on_validation_error():
    def bad_service(session):
        class S:
            def create_deck(self, name):
                raise ValueError("Deck name cannot be empty")

        return S()

    res = _patch_and_call(bad_service, "/decks/", method="post", json={"name": ""})
    assert res is not None
    assert res.status_code == 400
    assert res.json().get("detail") == "Deck name cannot be empty"


def test_get_deck_full_404_on_not_found():
    def bad_service(session):
        class S:
            def get_deck_with_cards(self, deck_id):
                raise ValueError("Deck not found")

        return S()

    res = _patch_and_call(bad_service, "/decks/1/full")
    assert res is not None
    assert res.status_code == 404
    assert res.json().get("detail") == "Deck not found"


def test_delete_deck_404_on_not_found():
    def bad_service(session):
        class S:
            def delete_deck(self, deck_id):
                raise ValueError("Deck not found")

        return S()

    res = _patch_and_call(bad_service, "/decks/1", method="delete")
    assert res is not None
    assert res.status_code == 404
    assert res.json().get("detail") == "Deck not found"
