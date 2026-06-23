import pytest

from app.db.base import Base
from app.db.engine import engine
from app.db.session import SessionLocal
from app.modules.cards.repository import CardRepository
from app.modules.decks.repository import DeckRepository
from app.modules.decks.services import DeckService

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_deck_creation(db):
    service = DeckService(DeckRepository(db))

    deck = service.create_deck("Spanish")

    assert deck.id is not None
    assert deck.name == "Spanish"


def test_deck_with_cards(db):
    deck_service = DeckService(DeckRepository(db))
    card_repo = CardRepository(db)

    deck = deck_service.create_deck("Languages")

    card_repo.create("Hola", "Hello", deck.id)
    card_repo.create("Adios", "Bye", deck.id)

    result = deck_service.get_deck_with_cards(deck.id)

    assert result["id"] == deck.id
    assert len(result["cards"]) == 2


def test_delete_deck(db):
    deck_service = DeckService(DeckRepository(db))

    deck = deck_service.create_deck("Temp")

    deck_service.delete_deck(deck.id)

    with pytest.raises(ValueError):
        deck_service.get_deck(deck.id)
