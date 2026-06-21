import pytest


def test_card_imports():
    import app.modules.cards.schemas
    import app.modules.cards.services
    import app.modules.cards.create
    #import app.modules.cards.api
    #import app.modules.cards.db


from app.modules.cards.schemas import CardSchema
def test_card_schema_can_be_instantiated():
    card = CardSchema()
    assert card is not None


def test_card_schema_fields():
    card = CardSchema(id=1, front="a", back="b")
    assert card.id == 1
    assert card.front == "a"
    assert card.back == "b"


from app.modules.cards.create import create_card
def test_create_card_function_exists():
    assert callable(create_card)


def test_create_card_function():
    card = create_card(id=1, front="a", back="b")
    assert card.id == 1
    assert card.front == "a"
    assert card.back == "b"