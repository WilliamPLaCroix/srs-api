# db/models.py

# IMPORTANT:
# This file should NOT define models.
# It only imports them so SQLAlchemy registers metadata.

from app.modules.cards.model import *
from app.modules.decks.model import *
from app.modules.reviews.model import *


__all__ = [
    "CardModel",
    "DeckModel",
    "ReviewModel",
]