from app.modules.decks.repository import DeckRepository
import logging

logger = logging.getLogger(__name__)

class DeckService:

    def __init__(self, repo: DeckRepository):
        self.repo = repo

    def create_deck(self, name: str):
        if not name.strip():
            raise ValueError("Deck name cannot be empty")

        return self.repo.create(name=name.strip())

    def get_deck(self, deck_id: int):
        deck = self.repo.get(deck_id)
        if not deck:
            raise ValueError("Deck not found")
        return deck

    def get_deck_with_cards(self, deck_id: int):
        deck = self.repo.get_with_cards(deck_id)
        if not deck:
            raise ValueError("Deck not found")

        # transform ORM → API shape
        return {
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

    def delete_deck(self, deck_id: int):
        deck = self.repo.get(deck_id)
        if not deck:
            raise ValueError("Deck not found")

        # cascade behavior happens via ORM config OR manual cleanup fallback
        self.repo.delete(deck)
        return {"status": "deleted"}