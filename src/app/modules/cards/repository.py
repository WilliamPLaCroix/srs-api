from sqlalchemy.orm import Session

from app.modules.cards.model import CardModel
import logging

logger = logging.getLogger(__name__)

class CardRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, front: str, back: str, deck_id: int) -> CardModel:
        card = CardModel(
            front=front,
            back=back,
            deck_id=deck_id
        )
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def get(self, card_id: int) -> CardModel | None:
        return self.db.query(CardModel).filter(CardModel.id == card_id).first()

    def list_by_deck(self, deck_id: int) -> list[CardModel]:
        return (
            self.db.query(CardModel)
            .filter(CardModel.deck_id == deck_id)
            .all()
        )
    
    def delete(self, card_id: int):
        card = self.get(card_id)
        if card:
            self.db.delete(card)
            self.db.commit()