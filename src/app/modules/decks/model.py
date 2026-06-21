from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class DeckModel(Base):
    __tablename__ = "decks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)

    cards = relationship(
        "CardModel",
        back_populates="deck",
        cascade="all, delete-orphan"
    )