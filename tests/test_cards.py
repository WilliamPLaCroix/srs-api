import pytest

from app.db.database import SessionLocal, Base, engine
from app.modules.cards.repository import CardRepository
from app.modules.cards.services import CardService
from app.modules.cards.schemas import CardCreate

from app import db  # ensure metadata registered
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_imports():
    from app.db.database import SessionLocal, Base, engine
    from app.modules.cards.repository import CardRepository
    from app.modules.cards.services import CardService
    from app.modules.cards.schemas import CardCreate

    from app import db  # ensure metadata registered


def test_create_card_flow(db):
    repo = CardRepository(db)
    service = CardService(repo)

    payload = CardCreate(
        front="What is FastAPI?",
        back="A Python web framework",
        deck_id=1
    )

    card = service.create_card(payload)

    assert card.id is not None
    assert card.front == "What is FastAPI?"
    assert card.deck_id == 1


def test_get_card_flow(db):
    repo = CardRepository(db)
    service = CardService(repo)

    created = service.create_card(
        CardCreate(front="A", back="B", deck_id=1)
    )

    fetched = service.get_card(created.id)

    assert fetched.id == created.id


def test_get_cards_by_deck(db):
    repo = CardRepository(db)
    service = CardService(repo)

    service.create_card(CardCreate(front="A", back="B", deck_id=99))
    service.create_card(CardCreate(front="C", back="D", deck_id=99))

    cards = service.get_cards_for_deck(99)

    assert len(cards) == 2

def test_delete_card(db):
    repo = CardRepository(db)
    service = CardService(repo)

    card = service.create_card(CardCreate(front="To delete", back="Delete me", deck_id=1))
    card_id = card.id

    service.delete_card(card_id)

    with pytest.raises(ValueError):
        service.get_card(card_id)