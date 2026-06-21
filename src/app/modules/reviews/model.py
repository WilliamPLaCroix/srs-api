from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    rating = Column(Integer)

    card_id = Column(Integer, ForeignKey("cards.id"))

    card = relationship("CardModel", back_populates="reviews")