from pydantic import BaseModel

class CardSchema(BaseModel):
    id: int
    front: str
    back: str