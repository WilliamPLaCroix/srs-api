import pytest

from app.modules.cards.model import Card
from app.modules.cards.repository import CardRepository
from tests.conftest import TestingSessionLocal


@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    # cleanup
    db.query(Card).delete()
    db.commit()
    db.close()


def test_create_get_list_delete(db):
    repo = CardRepository(db)

    # create
    card = repo.create(front="front", back="back", deck_id=1)
    assert card.id is not None
    assert card.front == "front"

    # get
    fetched = repo.get(card.id)
    assert fetched is not None and fetched.id == card.id

    # list_by_deck
    results = repo.list_by_deck(1)
    assert any(r.id == card.id for r in results)

    # delete
    repo.delete(card.id)
    assert repo.get(card.id) is None
