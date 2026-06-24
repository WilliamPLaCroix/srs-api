import logging

from sqlalchemy.orm import Session

from app.modules.cards.model import Card
from app.modules.reviews.model import Review

logger = logging.getLogger(__name__)


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db
        logger.debug("ReviewRepository initialized: Session=%s", type(db))

    def create(self, card_id: int, rating: int) -> Review:
        logger.debug("create called: card_id=%s rating=%s", card_id, rating)
        try:
            review = Review(card_id=card_id, rating=rating)
            self.db.add(review)
            self.db.commit()
            self.db.refresh(review)
            logger.info(
                "Review created: id=%s card_id=%s rating=%s",
                getattr(review, "id", None),
                card_id,
                rating,
            )
            return review
        except Exception:
            logger.exception("Failed to create review for card_id=%s rating=%s", card_id, rating)
            raise

    def get_by_deck(self, deck_id: int) -> list[Review]:
        logger.debug("get_by_deck called: deck_id=%s", deck_id)
        try:
            reviews = (
                self.db.query(Review)
                .join(Card, Review.card_id == Card.id)
                .filter(Card.deck_id == deck_id)
                .all()
            )
            logger.info("get_by_deck found %s reviews for deck_id=%s", len(reviews), deck_id)
            return reviews
        except Exception:
            logger.exception("Failed to fetch reviews for deck_id=%s", deck_id)
            raise

    def delete_by_deck(self, deck_id: int):
        logger.debug("delete_by_deck called: deck_id=%s", deck_id)
        try:
            reviews = self.get_by_deck(deck_id)
            if not reviews:
                logger.info("No reviews to delete for deck_id=%s", deck_id)
                return {"deleted_count": 0}

            deleted_count = 0
            for r in reviews:
                self.db.delete(r)
                deleted_count += 1
            self.db.commit()
            logger.info("Deleted %s reviews for deck_id=%s", deleted_count, deck_id)
            return {"deleted_count": deleted_count}
        except Exception:
            logger.exception("Failed to delete reviews for deck_id=%s", deck_id)
            raise

    def get_by_card(self, card_id: int) -> list[Review]:
        logger.debug("get_by_card called: card_id=%s", card_id)
        try:
            reviews = self.db.query(Review).filter(Review.card_id == card_id).all()
            logger.info("get_by_card found %s reviews for card_id=%s", len(reviews), card_id)
            return reviews
        except Exception:
            logger.exception("Failed to fetch reviews for card_id=%s", card_id)
            raise
