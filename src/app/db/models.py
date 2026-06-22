# db/models.py

# IMPORTANT:
# This file should NOT define models.
# It only imports them so SQLAlchemy registers metadata.

from sqlalchemy.orm import DeclarativeBase

# from app.modules.cards.model import *
# from app.modules.decks.model import *
# from app.modules.reviews.model import *


class Base(DeclarativeBase):
    pass


__all__ = [
    "Card",
    "Deck",
    "Review",
]