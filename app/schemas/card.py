from pydantic import BaseModel

class Card(BaseModel):
    id: int
    front: str
    back: str