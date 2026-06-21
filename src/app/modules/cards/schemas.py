from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CardBase(BaseModel):
    front: str = Field(..., min_length=1)
    back: str = Field(..., min_length=1)


class CardCreate(BaseModel):
    front: str
    back: str
    deck_id: int


class CardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None


class CardRead(BaseModel):
    id: int
    front: str
    back: str
    deck_id: int

    model_config = ConfigDict(from_attributes=True)