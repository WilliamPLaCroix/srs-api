from pydantic import BaseModel

class DeckSchema(BaseModel):
    id: int = None
    name: str = None