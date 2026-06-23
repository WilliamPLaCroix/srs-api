import pytest

from app.modules.cards.repository import CardRepository
from app.modules.decks.model import Deck
from app.modules.decks.repository import DeckRepository
from tests.conftest import TestingSessionLocal


@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    # cleanup
    db.query(Deck).delete()
    db.commit()
    db.close()


def test_create_get_get_with_cards_delete_flow(db):
    repo = DeckRepository(db)
    card_repo = CardRepository(db)

    # create deck
    deck = repo.create("Languages")
    assert deck.id is not None
    assert deck.name == "Languages"

    # get
    fetched = repo.get(deck.id)
    assert fetched is not None and fetched.id == deck.id

    # add cards
    card_repo.create("Hola", "Hello", deck.id)
    card_repo.create("Adios", "Bye", deck.id)

    # get with cards
    with_cards = repo.get_with_cards(deck.id)
    assert with_cards is not None
    assert len(getattr(with_cards, "cards", [])) == 2

    # delete
    repo.delete(with_cards)
    assert repo.get(deck.id) is None


def test_get_with_cards_not_found_returns_none(db):
    repo = DeckRepository(db)
    assert repo.get_with_cards(9999) is None


def test_create_raises_on_commit_error(db):
    repo = DeckRepository(db)

    def bad_commit():
        raise RuntimeError("commit failed")

    original_commit = db.commit
    db.commit = bad_commit
    try:
        with pytest.raises(RuntimeError):
            repo.create("X")
    finally:
        db.commit = original_commit


def test_get_raises_on_query_error(db):
    repo = DeckRepository(db)

    def bad_query(*args, **kwargs):
        raise RuntimeError("query failed")

    original_query = db.query
    db.query = bad_query
    try:
        with pytest.raises(RuntimeError):
            repo.get(1)
    finally:
        db.query = original_query


def test_delete_raises_on_commit_error(db):
    repo = DeckRepository(db)

    deck = repo.create("Temp")

    def bad_commit():
        raise RuntimeError("commit failed during delete")

    original_commit = db.commit
    db.commit = bad_commit
    try:
        with pytest.raises(RuntimeError):
            repo.delete(deck)
    finally:
        db.commit = original_commit


def test_get_with_cards_propagates_query_exception(db):
    repo = DeckRepository(db)

    def bad_query(*args, **kwargs):
        raise RuntimeError("query failed in get_with_cards")

    original_query = db.query
    db.query = bad_query
    try:
        with pytest.raises(RuntimeError):
            repo.get_with_cards(1)
    finally:
        db.query = original_query
