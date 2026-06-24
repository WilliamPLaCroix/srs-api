from pydantic import BaseModel, ConfigDict


class ReviewCreate(BaseModel):
    card_id: int
    rating: int  # 1–5


class ReviewRead(BaseModel):
    id: int
    card_id: int
    rating: int

    model_config = ConfigDict(from_attributes=True)


class DeckScore(BaseModel):
    deck_id: int
    average_score: float
    review_count: int


class CardScore(BaseModel):
    card_id: int
    average_score: float
    review_count: int
