from pydantic import BaseModel

class Review(BaseModel):
    card_id: int
    rating: int