from pydantic import BaseModel

class CardCreate(BaseModel):
    front: str
    back: str