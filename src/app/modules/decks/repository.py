from sqlalchemy.orm import Session, joinedload

from app.modules.decks.model import DeckModel
from app.modules.cards.model import CardModel
import logging

logger = logging.getLogger(__name__)

class DeckRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str) -> DeckModel:
        deck = DeckModel(name=name)
        self.db.add(deck)
        self.db.commit()
        self.db.refresh(deck)
        return deck

    def get(self, deck_id: int) -> DeckModel | None:
        return self.db.query(DeckModel).filter(DeckModel.id == deck_id).first()

    def get_with_cards(self, deck_id: int) -> DeckModel | None:
        return (
            self.db.query(DeckModel)
            .options(joinedload(DeckModel.cards))
            .filter(DeckModel.id == deck_id)
            .first()
        )

    def delete(self, deck: DeckModel):
        self.db.delete(deck)
        self.db.commit()