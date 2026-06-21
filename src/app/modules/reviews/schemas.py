from pydantic import BaseModel

class ReviewSchema(BaseModel):
    card_id: int = None
    rating: int = None