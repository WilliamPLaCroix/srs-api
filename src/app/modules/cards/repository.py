from sqlalchemy.orm import Session

from app.modules.cards.model import CardModel
import logging

logger = logging.getLogger(__name__)

class CardRepository:

    def __init__(self, db: Session):
        self.db = db
        logger.debug("CardRepository initialized: Session=%s", type(db))

    def create(self, front: str, back: str, deck_id: int) -> CardModel:
        logger.debug("create called: deck_id=%s front_len=%s back_len=%s", deck_id, len(front) if front else 0, len(back) if back else 0)
        try:
            card = CardModel(
                front=front,
                back=back,
                deck_id=deck_id
            )
            self.db.add(card)
            self.db.commit()
            self.db.refresh(card)
            logger.info("Card created: id=%s deck_id=%s", getattr(card, "id", None), deck_id)
            return card
        except Exception:
            logger.exception("Failed to create card for deck_id=%s", deck_id)
            raise

    def get(self, card_id: int) -> CardModel | None:
        logger.debug("get called: card_id=%s", card_id)
        try:
            card = self.db.query(CardModel).filter(CardModel.id == card_id).first()
        except Exception:
            logger.exception("Failed to fetch card_id=%s", card_id)
            raise

        if not card:
            logger.debug("get returned no result: card_id=%s", card_id)
        else:
            logger.debug("get fetched card: card_id=%s", card_id)
        return card

    def list_by_deck(self, deck_id: int) -> list[CardModel]:
        logger.debug("list_by_deck called: deck_id=%s", deck_id)
        try:
            results = (
                self.db.query(CardModel)
                .filter(CardModel.deck_id == deck_id)
                .all()
            )
            logger.info("list_by_deck found %s cards for deck_id=%s", len(results), deck_id)
            return results
        except Exception:
            logger.exception("Failed to list cards for deck_id=%s", deck_id)
            raise
    
    def delete(self, card_id: int):
        logger.debug("delete called: card_id=%s", card_id)
        try:
            card = self.get(card_id)
        except Exception:
            logger.exception("Failed to fetch card before delete: card_id=%s", card_id)
            raise

        if not card:
            logger.info("Attempted to delete non-existent card: card_id=%s", card_id)
            return

        try:
            self.db.delete(card)
            self.db.commit()
            logger.info("Deleted card: card_id=%s", card_id)
        except Exception:
            logger.exception("Failed to delete card_id=%s", card_id)
            raise