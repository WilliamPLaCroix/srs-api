from types import SimpleNamespace

import pytest

from app.modules.decks.services import DeckService


class FakeRepo:
    def __init__(self):
        self.store = {}

    def create(self, name):
        deck = SimpleNamespace(id=1, name=name)
        self.store[deck.id] = deck
        return deck

    def get(self, deck_id):
        return self.store.get(deck_id)

    def get_with_cards(self, deck_id):
        deck = self.store.get(deck_id)
        if not deck:
            return None
        deck.cards = [SimpleNamespace(id=1, front="a", back="b")]
        return deck

    def delete(self, deck):
        self.store.pop(deck.id, None)


def test_create_deck_validation_raises():
    repo = FakeRepo()
    svc = DeckService(repo)

    with pytest.raises(ValueError):
        svc.create_deck("")


def test_create_deck_success():
    repo = FakeRepo()
    svc = DeckService(repo)

    deck = svc.create_deck("Spanish")
    assert deck.id == 1
    assert deck.name == "Spanish"


def test_create_deck_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def create(self, name):
            raise RuntimeError("db error")

    svc = DeckService(BadRepo())

    with pytest.raises(RuntimeError):
        svc.create_deck("X")


def test_get_deck_not_found_raises():
    svc = DeckService(FakeRepo())
    with pytest.raises(ValueError):
        svc.get_deck(999)


def test_get_deck_success():
    repo = FakeRepo()
    svc = DeckService(repo)

    d = repo.create("A")
    res = svc.get_deck(d.id)
    assert res.id == d.id


def test_get_deck_repo_exception_propagates():
    class BadRepo(FakeRepo):
        def get(self, deck_id):
            raise RuntimeError("query failed")

    svc = DeckService(BadRepo())
    with pytest.raises(RuntimeError):
        svc.get_deck(1)


def test_get_deck_with_cards_not_found_raises():
    svc = DeckService(FakeRepo())
    with pytest.raises(ValueError):
        svc.get_deck_with_cards(999)


def test_get_deck_with_cards_success():
    repo = FakeRepo()
    svc = DeckService(repo)

    d = repo.create("X")
    res = svc.get_deck_with_cards(d.id)
    assert res["id"] == d.id
    assert isinstance(res["cards"], list)


def test_get_deck_with_cards_exception_propagates():
    class BadRepo(FakeRepo):
        def get_with_cards(self, deck_id):
            raise RuntimeError("query failed")

    svc = DeckService(BadRepo())
    with pytest.raises(RuntimeError):
        svc.get_deck_with_cards(1)


def test_delete_deck_not_found_raises():
    svc = DeckService(FakeRepo())
    with pytest.raises(ValueError):
        svc.delete_deck(9)


def test_delete_deck_success():
    repo = FakeRepo()
    svc = DeckService(repo)

    d = repo.create("Temp")
    res = svc.delete_deck(d.id)
    assert res["status"] == "deleted"


def test_delete_deck_delete_raises():
    class BadRepo(FakeRepo):
        def delete(self, deck):
            raise RuntimeError("delete failed")

    repo = BadRepo()
    # ensure a deck exists so get() returns it and delete() is called
    repo.create("ToDelete")
    svc = DeckService(repo)
    with pytest.raises(RuntimeError):
        svc.delete_deck(1)


def test_delete_deck_get_raises():
    class BadRepo(FakeRepo):
        def get(self, deck_id):
            raise RuntimeError("get failed before delete")

    svc = DeckService(BadRepo())
    with pytest.raises(RuntimeError):
        svc.delete_deck(1)
