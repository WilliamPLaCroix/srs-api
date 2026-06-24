import logging

from sqlalchemy.orm import Session, joinedload

from app.modules.decks.model import Deck

logger = logging.getLogger(__name__)


class DeckRepository:
    def __init__(self, db: Session):
        self.db = db
        logger.debug("DeckRepository initialized: Session=%s", type(db))

    def create(self, name: str) -> Deck:
        logger.debug("create called: name=%s", name)
        try:
            deck = Deck(name=name)
            self.db.add(deck)
            self.db.commit()
            self.db.refresh(deck)
            logger.info("Deck created: id=%s name=%s", getattr(deck, "id", None), name)
            return deck
        except Exception:
            logger.exception("Failed to create deck with name=%s", name)
            raise

    def get(self, deck_id: int) -> Deck | None:
        logger.debug("get called: deck_id=%s", deck_id)
        try:
            deck = self.db.query(Deck).filter(Deck.id == deck_id).first()
        except Exception:
            logger.exception("Failed to fetch deck_id=%s", deck_id)
            raise

        if not deck:
            logger.debug("get returned no result: deck_id=%s", deck_id)
        else:
            logger.debug("get fetched deck: deck_id=%s", deck_id)
        return deck

    def get_with_cards(self, deck_id: int) -> Deck | None:
        logger.debug("get_with_cards called: deck_id=%s", deck_id)
        try:
            deck = (
                self.db.query(Deck)
                .options(joinedload(Deck.cards))
                .filter(Deck.id == deck_id)
                .first()
            )
        except Exception:
            logger.exception("Failed to fetch deck with cards for deck_id=%s", deck_id)
            raise

        if not deck:
            logger.info("Deck not found (with cards): deck_id=%s", deck_id)
            return None

        card_count = len(getattr(deck, "cards", []))
        logger.info("Fetched deck with cards: deck_id=%s card_count=%s", deck_id, card_count)
        return deck

    def delete(self, deck: Deck):
        logger.debug("delete called: deck_id=%s", getattr(deck, "id", None))
        try:
            self.db.delete(deck)
            self.db.commit()
            logger.info("Deleted deck: deck_id=%s", getattr(deck, "id", None))
        except Exception:
            logger.exception("Failed to delete deck_id=%s", getattr(deck, "id", None))
            raise

    def update(self, deck_id: int, name: str | None = None) -> Deck | None:
        logger.debug("update called: deck_id=%s name_present=%s", deck_id, bool(name))
        try:
            deck = self.get(deck_id)
        except Exception:
            logger.exception("Failed to fetch deck before update: deck_id=%s", deck_id)
            raise

        if not deck:
            logger.info("Attempted to update non-existent deck: deck_id=%s", deck_id)
            return None

        if name is not None:
            deck.name = name

        try:
            self.db.add(deck)
            self.db.commit()
            self.db.refresh(deck)
            logger.info("Updated deck: deck_id=%s", getattr(deck, "id", None))
            return deck
        except Exception:
            logger.exception("Failed to update deck_id=%s", deck_id)
            raise
