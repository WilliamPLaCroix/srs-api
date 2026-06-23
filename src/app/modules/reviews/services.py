import logging
from statistics import mean

from app.modules.reviews.repository import ReviewRepository

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, repo: ReviewRepository):
        self.repo = repo

    def create_review(self, card_id: int, rating: int):
        logger.debug("create_review called: card_id=%s rating=%s", card_id, rating)

        if rating < 1 or rating > 5:
            logger.warning(
                "create_review validation failed: rating out of range (1-5): %s for card_id=%s",
                rating,
                card_id,
            )
            raise ValueError("Rating must be 1–5")

        try:
            review = self.repo.create(card_id, rating)
            logger.info(
                "Review created: card_id=%s rating=%s review_id=%s",
                card_id,
                rating,
                getattr(review, "id", None),
            )
            return review
        except Exception:
            logger.exception("Error creating review for card_id=%s rating=%s", card_id, rating)
            raise

    def compute_deck_score(self, deck_id: int):
        logger.debug("compute_deck_score called: deck_id=%s", deck_id)
        try:
            reviews = self.repo.get_by_deck(deck_id)
        except Exception:
            logger.exception("Failed to fetch reviews for deck_id=%s", deck_id)
            raise

        if not reviews:
            logger.info("No reviews found for deck_id=%s; returning zeroed score", deck_id)
            return {"deck_id": deck_id, "average_score": 0.0, "review_count": 0}

        scores = [r.rating for r in reviews]
        average = round(mean(scores), 2)
        count = len(scores)
        logger.info(
            "Computed deck score: deck_id=%s average_score=%s review_count=%s",
            deck_id,
            average,
            count,
        )

        return {"deck_id": deck_id, "average_score": average, "review_count": count}

    def delete_deck_reviews(self, deck_id: int):
        logger.debug("delete_deck_reviews called: deck_id=%s", deck_id)
        try:
            result = self.repo.delete_by_deck(deck_id)
            logger.info(
                "Deleted reviews for deck_id=%s result=%s",
                deck_id,
                getattr(result, "deleted_count", result),
            )
            return result
        except Exception:
            logger.exception("Failed to delete reviews for deck_id=%s", deck_id)
            raise
