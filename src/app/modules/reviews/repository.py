from sqlalchemy.orm import Session

from app.modules.reviews.model import ReviewModel
from app.modules.cards.model import CardModel


class ReviewRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, card_id: int, rating: int) -> ReviewModel:
        review = ReviewModel(card_id=card_id, rating=rating)
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_by_deck(self, deck_id: int) -> list[ReviewModel]:
        return (
            self.db.query(ReviewModel)
            .join(CardModel, ReviewModel.card_id == CardModel.id)
            .filter(CardModel.deck_id == deck_id)
            .all()
        )

    def delete_by_deck(self, deck_id: int):
        reviews = self.get_by_deck(deck_id)
        for r in reviews:
            self.db.delete(r)
        self.db.commit()