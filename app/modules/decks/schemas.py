from pydantic import BaseModel

class DeckSchema(BaseModel):
    id: int
    name: str