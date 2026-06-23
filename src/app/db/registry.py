"""
Explicit SQLAlchemy model registry.

Alembic and engine initialization MUST import this module.
"""

from app.modules.cards.model import Card
from app.modules.decks.model import Deck
from app.modules.reviews.model import Review

__all__ = [
    "Card",
    "Deck",
    "Review",
]