from pydantic import BaseModel

class CardSchema(BaseModel):
    id: int = None
    front: str = None
    back: str = None