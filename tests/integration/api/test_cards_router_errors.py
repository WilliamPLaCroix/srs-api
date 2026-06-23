from fastapi.testclient import TestClient

from app.main import app
from app.modules.cards import router as cards_router

client = TestClient(app)


def test_create_card_500_on_service_error():
    def _bad_service(session):
        class S:
            def create_card(self, payload):
                raise RuntimeError("service failure")

        return S()

    original = cards_router.get_card_service
    cards_router.get_card_service = _bad_service
    try:
        res = client.post("/cards/", json={"front": "f", "back": "b", "deck_id": 1})
        assert res.status_code == 500
        assert res.json().get("detail") == "Internal server error"
    finally:
        cards_router.get_card_service = original


def test_get_card_500_on_service_error():
    def _bad_service(session):
        class S:
            def get_card(self, card_id):
                raise RuntimeError("service failure")

        return S()

    original = cards_router.get_card_service
    cards_router.get_card_service = _bad_service
    try:
        res = client.get("/cards/1")
        assert res.status_code == 500
        assert res.json().get("detail") == "Internal server error"
    finally:
        cards_router.get_card_service = original


def test_list_cards_500_on_service_error():
    def _bad_service(session):
        class S:
            def get_cards_for_deck(self, deck_id):
                raise RuntimeError("service failure")

        return S()

    original = cards_router.get_card_service
    cards_router.get_card_service = _bad_service
    try:
        res = client.get("/cards/deck/1")
        assert res.status_code == 500
        assert res.json().get("detail") == "Internal server error"
    finally:
        cards_router.get_card_service = original


def test_delete_card_500_on_service_error():
    def _bad_service(session):
        class S:
            def delete_card(self, card_id):
                raise RuntimeError("service failure")

        return S()

    original = cards_router.get_card_service
    cards_router.get_card_service = _bad_service
    try:
        res = client.delete("/cards/1")
        assert res.status_code == 500
        assert res.json().get("detail") == "Internal server error"
    finally:
        cards_router.get_card_service = original


def test_create_card_400_on_validation_error():
    def _bad_service(session):
        class S:
            def create_card(self, payload):
                raise ValueError("invalid payload")

        return S()

    original = cards_router.get_card_service
    cards_router.get_card_service = _bad_service
    try:
        res = client.post("/cards/", json={"front": "", "back": "", "deck_id": 1})
        assert res.status_code == 400
        assert res.json().get("detail") == "invalid payload"
    finally:
        cards_router.get_card_service = original


def test_delete_card_404_on_not_found():
    def _bad_service(session):
        class S:
            def delete_card(self, card_id):
                raise ValueError("Card not found")

        return S()

    original = cards_router.get_card_service
    cards_router.get_card_service = _bad_service
    try:
        res = client.delete("/cards/1")
        assert res.status_code == 404
        assert res.json().get("detail") == "Card not found"
    finally:
        cards_router.get_card_service = original
