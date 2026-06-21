from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    front = Column(String)
    back = Column(String)

    deck_id = Column(Integer, ForeignKey("decks.id"))

    deck = relationship(
        "DeckModel",
        back_populates="cards"
    )

    reviews = relationship(
        "ReviewModel",
        cascade="all, delete",
        back_populates="card"
    )