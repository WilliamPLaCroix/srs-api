from pydantic import BaseModel, ConfigDict


class DeckCreate(BaseModel):
    name: str


class DeckRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DeckWithCards(BaseModel):
    id: int
    name: str
    cards: list[dict]


class DeckUpdate(BaseModel):
    name: str | None = None
