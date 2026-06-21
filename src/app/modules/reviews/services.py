from statistics import mean

from app.modules.reviews.repository import ReviewRepository
from app.modules.cards.model import CardModel


class ReviewService:

    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    def create_review(self, card_id: int, rating: int):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be 1–5")

        return self.repo.create(card_id, rating)

    def compute_deck_score(self, deck_id: int):
        reviews = self.repo.get_by_deck(deck_id)

        if not reviews:
            return {
                "deck_id": deck_id,
                "average_score": 0.0,
                "review_count": 0
            }

        scores = [r.rating for r in reviews]

        return {
            "deck_id": deck_id,
            "average_score": round(mean(scores), 2),
            "review_count": len(scores)
        }

    def delete_deck_reviews(self, deck_id: int):
        self.repo.delete_by_deck(deck_id)