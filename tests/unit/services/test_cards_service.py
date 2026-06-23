from types import SimpleNamespace

import pytest

from app.modules.cards.schemas import CardCreate
from app.modules.cards.services import CardService


class FakeRepo:
    def __init__(self):
        self.calls = {}

    def create(self, front, back, deck_id):
        self.calls["create"] = (front, back, deck_id)
        return SimpleNamespace(id=1, front=front, back=back, deck_id=deck_id)

    def get(self, card_id):
        self.calls["get"] = (card_id,)
        return SimpleNamespace(id=card_id, front="f", back="b", deck_id=1)

    def list_by_deck(self, deck_id):
        self.calls["list_by_deck"] = (deck_id,)
        return [SimpleNamespace(id=1, front="a", back="b", deck_id=deck_id)]

    def delete(self, card_id):
        self.calls["delete"] = (card_id,)
        return None


def test_create_card_validation_raises():
    repo = FakeRepo()
    svc = CardService(repo)

    payload = CardCreate(front="", back="", deck_id=1)
    with pytest.raises(ValueError):
        svc.create_card(payload)


def test_create_card_success():
    repo = FakeRepo()
    svc = CardService(repo)

    payload = CardCreate(front="Q", back="A", deck_id=2)
    card = svc.create_card(payload)

    assert card.id == 1
    assert repo.calls["create"] == ("Q", "A", 2)


def test_create_card_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def create(self, front, back, deck_id):
            raise RuntimeError("db error")

    repo = BadRepo()
    svc = CardService(repo)

    with pytest.raises(RuntimeError):
        svc.create_card(CardCreate(front="x", back="y", deck_id=1))


def test_get_card_not_found_raises():
    class NoRepo(FakeRepo):
        def get(self, card_id):
            return None

    repo = NoRepo()
    svc = CardService(repo)

    with pytest.raises(ValueError):
        svc.get_card(42)


def test_get_card_success():
    repo = FakeRepo()
    svc = CardService(repo)

    card = svc.get_card(5)
    assert card.id == 5


def test_get_card_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def get(self, card_id):
            raise RuntimeError("query error")

    repo = BadRepo()
    svc = CardService(repo)

    with pytest.raises(RuntimeError):
        svc.get_card(1)


def test_get_cards_for_deck_success():
    repo = FakeRepo()
    svc = CardService(repo)

    res = svc.get_cards_for_deck(7)
    assert isinstance(res, list)
    assert repo.calls["list_by_deck"] == (7,)


def test_get_cards_for_deck_exception_propagates():
    class BadRepo(FakeRepo):
        def list_by_deck(self, deck_id):
            raise RuntimeError("list error")

    repo = BadRepo()
    svc = CardService(repo)

    with pytest.raises(RuntimeError):
        svc.get_cards_for_deck(1)


def test_delete_card_not_found_raises():
    class NoRepo(FakeRepo):
        def get(self, card_id):
            return None

    repo = NoRepo()
    svc = CardService(repo)

    with pytest.raises(ValueError):
        svc.delete_card(9)


def test_delete_card_success():
    repo = FakeRepo()
    svc = CardService(repo)

    res = svc.delete_card(1)
    assert res == {"status": "deleted"}
    assert repo.calls["get"] == (1,)
    assert repo.calls["delete"] == (1,)


def test_delete_card_get_raises():
    class BadRepo(FakeRepo):
        def get(self, card_id):
            raise RuntimeError("get failed")

    repo = BadRepo()
    svc = CardService(repo)

    with pytest.raises(RuntimeError):
        svc.delete_card(1)


def test_delete_card_delete_raises():
    class BadRepo(FakeRepo):
        def delete(self, card_id):
            raise RuntimeError("delete failed")

    repo = BadRepo()
    svc = CardService(repo)

    with pytest.raises(RuntimeError):
        svc.delete_card(1)
