import pytest

from app.modules.cards.model import Card
from app.modules.cards.repository import CardRepository
from app.modules.decks.model import Deck
from app.modules.decks.repository import DeckRepository
from app.modules.reviews.model import Review
from app.modules.reviews.repository import ReviewRepository
from tests.conftest import TestingSessionLocal


@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    # cleanup
    db.query(Review).delete()
    db.query(Card).delete()
    db.query(Deck).delete()
    db.commit()
    db.close()


def test_create_get_by_deck_and_delete_by_deck(db):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_repo = ReviewRepository(db)

    deck = deck_repo.create("Science")
    card = card_repo.create("Q", "A", deck.id)

    review_repo.create(card.id, 5)
    review_repo.create(card.id, 3)

    reviews = review_repo.get_by_deck(deck.id)
    assert len(reviews) == 2

    result = review_repo.delete_by_deck(deck.id)
    assert result["deleted_count"] == 2

    remaining = review_repo.get_by_deck(deck.id)
    assert len(remaining) == 0


def test_delete_by_deck_no_reviews_returns_zero(db):
    deck_repo = DeckRepository(db)
    review_repo = ReviewRepository(db)

    deck = deck_repo.create("Empty")

    res = review_repo.delete_by_deck(deck.id)
    assert res["deleted_count"] == 0


def test_create_raises_on_commit_error(db):
    review_repo = ReviewRepository(db)

    original_commit = db.commit

    def bad_commit():
        raise RuntimeError("commit failed")

    db.commit = bad_commit
    try:
        with pytest.raises(RuntimeError):
            review_repo.create(1, 5)
    finally:
        db.commit = original_commit


def test_get_by_deck_raises_on_query_error(db):
    review_repo = ReviewRepository(db)

    original_query = db.query

    def bad_query(*args, **kwargs):
        raise RuntimeError("query failed")

    db.query = bad_query
    try:
        with pytest.raises(RuntimeError):
            review_repo.get_by_deck(1)
    finally:
        db.query = original_query


def test_delete_by_deck_propagates_commit_error(db):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_repo = ReviewRepository(db)

    deck = deck_repo.create("Temp")
    card = card_repo.create("Q", "A", deck.id)
    review_repo.create(card.id, 5)

    original_commit = db.commit

    def bad_commit():
        raise RuntimeError("commit failed during delete")

    db.commit = bad_commit
    try:
        with pytest.raises(RuntimeError):
            review_repo.delete_by_deck(deck.id)
    finally:
        db.commit = original_commit
