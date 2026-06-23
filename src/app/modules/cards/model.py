from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    front: Mapped[str] = mapped_column(String(255), nullable=False)
    back: Mapped[str] = mapped_column(Text, nullable=False)

    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=False)

    deck = relationship("Deck", back_populates="cards")
    reviews = relationship("Review", back_populates="card", cascade="all, delete-orphan")
