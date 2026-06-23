import logging

from app.modules.decks.repository import DeckRepository

logger = logging.getLogger(__name__)

class DeckService:

    def __init__(self, repo: DeckRepository):
        self.repo = repo

    def create_deck(self, name: str):
        logger.debug("create_deck called: name=%s", name)

        if not name.strip():
            logger.warning("create_deck validation failed: empty name")
            raise ValueError("Deck name cannot be empty")

        try:
            deck = self.repo.create(name=name.strip())
            logger.info("Deck created: id=%s name=%s", getattr(deck, "id", None), name.strip())
            return deck
        except Exception:
            logger.exception("Error creating deck with name=%s", name)
            raise

    def get_deck(self, deck_id: int):
        logger.debug("get_deck called: deck_id=%s", deck_id)
        try:
            deck = self.repo.get(deck_id)
        except Exception:
            logger.exception("Failed to fetch deck_id=%s", deck_id)
            raise

        if not deck:
            logger.info("Deck not found: deck_id=%s", deck_id)
            raise ValueError("Deck not found")

        logger.debug("Deck fetched: deck_id=%s", deck_id)
        return deck

    def get_deck_with_cards(self, deck_id: int):
        logger.debug("get_deck_with_cards called: deck_id=%s", deck_id)
        try:
            deck = self.repo.get_with_cards(deck_id)
        except Exception:
            logger.exception("Failed to fetch deck with cards for deck_id=%s", deck_id)
            raise

        if not deck:
            logger.info("Deck not found (with cards): deck_id=%s", deck_id)
            raise ValueError("Deck not found")

        card_count = len(getattr(deck, "cards", []))
        logger.debug("Transforming deck to API shape: deck_id=%s card_count=%s", deck_id, card_count)

        # transform ORM → API shape
        result = {
            "id": deck.id,
            "name": deck.name,
            "cards": [
                {
                    "id": c.id,
                    "front": c.front,
                    "back": c.back
                }
                for c in deck.cards
            ]
        }

        logger.info("Deck with cards prepared: deck_id=%s card_count=%s", deck_id, card_count)
        return result

    def delete_deck(self, deck_id: int):
        logger.debug("delete_deck called: deck_id=%s", deck_id)
        try:
            deck = self.repo.get(deck_id)
        except Exception:
            logger.exception("Failed to fetch deck before delete: deck_id=%s", deck_id)
            raise

        if not deck:
            logger.info("Attempted to delete non-existent deck: deck_id=%s", deck_id)
            raise ValueError("Deck not found")

        try:
            # cascade behavior happens via ORM config OR manual cleanup fallback
            self.repo.delete(deck)
            logger.info("Deleted deck: deck_id=%s", deck_id)
            return {"status": "deleted"}
        except Exception:
            logger.exception("Failed to delete deck_id=%s", deck_id)
            raise