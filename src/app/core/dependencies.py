from sqlalchemy.orm import Session
from fastapi import Depends

from app.db.database import get_db

from app.modules.cards.repository import CardRepository
from app.modules.cards.services import CardService

from app.modules.decks.repository import DeckRepository
from app.modules.decks.services import DeckService

from app.modules.reviews.repository import ReviewRepository
from app.modules.reviews.services import ReviewService


# -----------------------
# DB session dependency
# -----------------------
def get_session() -> Session:
    yield from get_db()


# -----------------------
# Cards
# -----------------------
def get_card_service(session: Session = Depends(get_session)) -> CardService:
    repo = CardRepository(session)
    return CardService(repo)


# -----------------------
# Decks
# -----------------------
def get_deck_service(session: Session = Depends(get_session)) -> DeckService:
    repo = DeckRepository(session)
    return DeckService(repo)


# -----------------------
# Reviews
# -----------------------
def get_review_service(session: Session = Depends(get_session)) -> ReviewService:
    repo = ReviewRepository(session)
    return ReviewService(repo)