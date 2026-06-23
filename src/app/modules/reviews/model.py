from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), nullable=False)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 0–5 scale
    reviewed_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    card = relationship("Card", back_populates="reviews")