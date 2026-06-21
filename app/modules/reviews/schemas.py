from pydantic import BaseModel

class ReviewSchema(BaseModel):
    card_id: int
    rating: int