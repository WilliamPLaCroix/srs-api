import logging

from app.modules.cards.repository import CardRepository
from app.modules.cards.schemas import CardCreate, CardUpdate

logger = logging.getLogger(__name__)


class CardService:
    def __init__(self, repo: CardRepository):
        self.repo = repo

    def create_card(self, data: CardCreate):
        logger.debug(
            "create_card called: deck_id=%s front_present=%s back_present=%s",
            data.deck_id,
            bool(data.front),
            bool(data.back),
        )
        # business rule example (simple but real)
        if not data.front or not data.back:
            logger.warning(
                "create_card validation failed: missing front/back: deck_id=%s", data.deck_id
            )
            raise ValueError("Card must have front and back")

        try:
            card = self.repo.create(
                front=data.front.strip(),
                back=data.back.strip(),
                deck_id=data.deck_id,
            )
            logger.info("Card created: id=%s deck_id=%s", getattr(card, "id", None), data.deck_id)
            return card
        except Exception:
            logger.exception(
                "Error creating card for deck_id=%s front=%s", data.deck_id, data.front
            )
            raise

    def get_card(self, card_id: int):
        logger.debug("get_card called: card_id=%s", card_id)
        try:
            card = self.repo.get(card_id)
        except Exception:
            logger.exception("Failed to fetch card_id=%s", card_id)
            raise

        if not card:
            logger.info("Card not found: card_id=%s", card_id)
            raise ValueError("Card not found")

        logger.debug("Card fetched: card_id=%s", card_id)
        return card

    def get_cards_for_deck(self, deck_id: int):
        logger.debug("get_cards_for_deck called: deck_id=%s", deck_id)
        try:
            cards = self.repo.list_by_deck(deck_id)
            logger.info("Fetched %s cards for deck_id=%s", len(cards), deck_id)
            return cards
        except Exception:
            logger.exception("Failed to list cards for deck_id=%s", deck_id)
            raise

    def delete_card(self, card_id: int):
        logger.debug("delete_card called: card_id=%s", card_id)
        try:
            card = self.repo.get(card_id)
        except Exception:
            logger.exception("Failed to fetch card before delete: card_id=%s", card_id)
            raise

        if not card:
            logger.info("Attempted to delete non-existent card: card_id=%s", card_id)
            raise ValueError("Card not found")

        try:
            self.repo.delete(card_id)
            logger.info("Deleted card: card_id=%s", card_id)
            return {"status": "deleted"}
        except Exception:
            logger.exception("Failed to delete card_id=%s", card_id)
            raise

    def update_card(self, card_id: int, data: CardUpdate):
        logger.debug(
            "update_card called: card_id=%s front_present=%s back_present=%s",
            card_id,
            bool(getattr(data, "front", None)),
            bool(getattr(data, "back", None)),
        )

        # Require at least one field to update
        if getattr(data, "front", None) is None and getattr(data, "back", None) is None:
            logger.warning("update_card called with no updatable fields: card_id=%s", card_id)
            raise ValueError("No fields to update")

        try:
            front = (
                data.front.strip()
                if (getattr(data, "front", None) is not None and data.front is not None)
                else None
            )
            back = (
                data.back.strip()
                if (getattr(data, "back", None) is not None and data.back is not None)
                else None
            )
            card = self.repo.update(card_id, front=front, back=back)
        except Exception:
            logger.exception("Failed to update card_id=%s", card_id)
            raise

        if not card:
            logger.info("Card not found for update: card_id=%s", card_id)
            raise ValueError("Card not found")

        logger.info("Card updated: card_id=%s", card_id)
        return card
