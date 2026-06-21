import pytest


def test_deck_imports():
    import app.modules.decks.schemas
    #import app.modules.decks.services
    #import app.modules.decks.create
    #import app.modules.decks.api
    #import app.modules.decks.db


from app.modules.decks.schemas import DeckSchema
def test_deck_schema_can_be_instantiated():
    deck = DeckSchema()
    assert deck is not None


def test_deck_schema_fields():
    deck = DeckSchema(id=1, name="Test Deck")
    assert deck.id == 1
    assert deck.name == "Test Deck"

# from app.modules.decks.create import create_deck
# def test_create_deck_function_exists():
#     assert callable(create_deck)