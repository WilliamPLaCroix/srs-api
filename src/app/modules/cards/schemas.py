from pydantic import BaseModel, ConfigDict, Field


class CardBase(BaseModel):
    front: str = Field(..., min_length=1)
    back: str = Field(..., min_length=1)


class CardCreate(BaseModel):
    front: str
    back: str
    deck_id: int


class CardUpdate(BaseModel):
    front: str | None = None
    back: str | None = None


class CardRead(BaseModel):
    id: int
    front: str
    back: str
    deck_id: int

    model_config = ConfigDict(from_attributes=True)
