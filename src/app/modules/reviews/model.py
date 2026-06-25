from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ReviewLog(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), nullable=False)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 0–5 scale
    # interval_before: int
    # interval_after: int

    # ease_before: float
    # ease_after: float

    # response_time_ms: int | None = None
    reviewed_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())

    card = relationship("Card", back_populates="reviews")


Review = ReviewLog  # Alias for backward compatibility
