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


def test_create_raises_on_commit_error(db):
    repo = CardRepository(db)

    # break commit
    def bad_commit():
        raise RuntimeError("commit failed")

    original_commit = db.commit
    db.commit = bad_commit
    try:
        with pytest.raises(RuntimeError):
            repo.create("f", "b", 1)
    finally:
        db.commit = original_commit


def test_get_raises_on_query_error(db):
    repo = CardRepository(db)

    def bad_query(*args, **kwargs):
        raise RuntimeError("query failed")

    original_query = db.query
    db.query = bad_query
    try:
        with pytest.raises(RuntimeError):
            repo.get(1)
    finally:
        db.query = original_query


def test_list_by_deck_raises_on_query_error(db):
    repo = CardRepository(db)

    def bad_query(*args, **kwargs):
        raise RuntimeError("query failed")

    original_query = db.query
    db.query = bad_query
    try:
        with pytest.raises(RuntimeError):
            repo.list_by_deck(1)
    finally:
        db.query = original_query


def test_delete_nonexistent_returns_none(db):
    repo = CardRepository(db)

    # ensure no card with this id
    assert repo.get(9999) is None

    result = repo.delete(9999)

    assert result is None


def test_delete_raises_on_commit_error_after_fetch(db):
    repo = CardRepository(db)

    # create a card normally
    card = repo.create("x", "y", 1)

    # break commit during delete
    def bad_commit():
        raise RuntimeError("commit failed during delete")

    original_commit = db.commit
    db.commit = bad_commit
    try:
        with pytest.raises(RuntimeError):
            repo.delete(card.id)
    finally:
        db.commit = original_commit


def test_delete_propagates_get_exception(db):
    repo = CardRepository(db)

    # make repo.get raise when called from delete()
    def bad_get(card_id):
        raise RuntimeError("get failed in delete")

    original_get = repo.get
    repo.get = bad_get
    try:
        with pytest.raises(RuntimeError):
            repo.delete(1)
    finally:
        repo.get = original_get
