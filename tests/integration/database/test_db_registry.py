def test_registry_exports_models():
    import importlib

    registry = importlib.import_module("app.db.registry")

    # Ensure the registry exposes expected names
    assert "Card" in registry.__all__
    assert "Deck" in registry.__all__
    assert "Review" in registry.__all__

    # Attributes should be present on the module
    assert hasattr(registry, "Card")
    assert hasattr(registry, "Deck")
    assert hasattr(registry, "Review")

    # Basic sanity checks on the exported objects
    Card = registry.Card
    Deck = registry.Deck
    Review = registry.Review

    # They should be classes (SQLAlchemy models are classes)
    assert isinstance(Card, type)
    assert isinstance(Deck, type)
    assert isinstance(Review, type)

    # Ensure they have a __tablename__ attribute (typical for declarative models)
    assert hasattr(Card, "__tablename__")
    assert hasattr(Deck, "__tablename__")
    assert hasattr(Review, "__tablename__")
