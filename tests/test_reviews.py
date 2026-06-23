import pytest

from app.db.base import Base
from app.db.session import SessionLocal
from app.db.engine import engine

from app.modules.cards.repository import CardRepository
from app.modules.decks.repository import DeckRepository
from app.modules.reviews.repository import ReviewRepository
from app.modules.reviews.services import ReviewService

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_review_scoring(db):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_service = ReviewService(ReviewRepository(db))

    deck = deck_repo.create("Science")

    card = card_repo.create("Q", "A", deck.id)

    review_service.create_review(card.id, 5)
    review_service.create_review(card.id, 3)

    score = review_service.compute_deck_score(deck.id)

    assert score["average_score"] == 4.0
    assert score["review_count"] == 2


def test_empty_deck_score(db):
    review_service = ReviewService(ReviewRepository(db))

    score = review_service.compute_deck_score(999)

    assert score["average_score"] == 0.0
    assert score["review_count"] == 0


def test_cascade_delete_reviews(db):
    deck_repo = DeckRepository(db)
    card_repo = CardRepository(db)
    review_service = ReviewService(ReviewRepository(db))

    deck = deck_repo.create("Temp")

    card = card_repo.create("Q", "A", deck.id)

    review_service.create_review(card.id, 5)

    # delete deck-level cleanup
    review_service.delete_deck_reviews(deck.id)

    score = review_service.compute_deck_score(deck.id)

    assert score["review_count"] == 0