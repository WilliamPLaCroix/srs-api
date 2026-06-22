from app.modules.cards.repository import CardRepository
from app.modules.cards.schemas import CardCreate
import logging

logger = logging.getLogger(__name__)

class CardService:

    def __init__(self, repo: CardRepository):
        self.repo = repo

    def create_card(self, data: CardCreate):
        # business rule example (simple but real)
        if not data.front or not data.back:
            raise ValueError("Card must have front and back")

        return self.repo.create(
            front=data.front.strip(),
            back=data.back.strip(),
            deck_id=data.deck_id,
        )

    def get_card(self, card_id: int):
        card = self.repo.get(card_id)
        if not card:
            raise ValueError("Card not found")
        return card

    def get_cards_for_deck(self, deck_id: int):
        return self.repo.list_by_deck(deck_id)
    
    def delete_card(self, card_id: int):
        if not self.repo.get(card_id):
            raise ValueError("Card not found")
        self.repo.delete(card_id)
